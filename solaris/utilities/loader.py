from lxml import etree

from django.conf import settings
from django.db import transaction
from django.utils.html import strip_tags

from solaris.warbook.mech.models import MechDesign, MechLocation, MechDesignLocation
from solaris.utilities import translate

from .parser import SSWMech, SSWParseError
from .forms import MechValidationForm, LocationValidationForm, MechEquipmentForm, MountingForm

def print_errors(errors):
    for (key, value) in errors.items():
        print '\t%s: %s' % (key, strip_tags('%s' % value))
        
class MechLoader(object):
    
    def load_locations(self, mech, mech_model):
        locations = {}
        
        for (ssw_code, armour) in mech.armour.armour.items():
            loc_code = self.location_map[ssw_code]
            loc_model = MechLocation.objects.get(location=loc_code)
                
            try:
                mechlocation = MechDesignLocation.objects.get(mech=mech_model, location=loc_model)
            except MechDesignLocation.DoesNotExist:
                mechlocation = None   
                          
            location_data = dict()
            location_data['mech'] = mech_model.id
            location_data['location'] = loc_model.id
            location_data['armour'] = armour
            location_data['structure'] =  loc_model.structure(mech_model.tonnage)
            
            form = LocationValidationForm(location_data, instance=mechlocation)
            if form.is_valid():
                form.save()
            else:
                raise SSWParseError(mech, form.errors)
            
            locations[loc_code] = MechDesignLocation.objects.get(mech=mech_model, location=loc_model)
    
        return locations
    
    def load_equipment(self, mech, mech_id, equipment, mechlocations):
        equipment['mech'] = mech_id
        eq_form = MechEquipmentForm(equipment)
        
        if eq_form.is_valid():
            eq_form.save()
                    
            for ssw_loc, mount in equipment.mountings.items():
                loc_code = self.location_map[ssw_loc]
                
                mount['equipment'] = eq_form.instance.id
                mount['location'] = mechlocations[loc_code].id
                mount_form = MountingForm(mount)
                if mount_form.is_valid():
                    mount_form.save()
                else:
                    raise SSWParseError(mech, mount_form.errors)
            eq_form.save()
        else:
            raise SSWParseError(mech, eq_form.errors)
        
                
    @transaction.commit_manually
    def load_mech(self, sswfile):
        try:
            filename = '%s/%s' % (settings.SSW_STOCK_MECHS_ROOT, sswfile)
            fd = open(filename,'rb')
            
            sswXML = etree.parse(fd)
            mech = SSWMech( sswXML.xpath('/mech')[0], sswfile )
            
            if mech.type != 'BattleMech' or mech['tech_base'] != 'I' or int(mech['tonnage']) < 20:
                transaction.rollback()
                return 
            
            print "Importing %s ( %s / %s )" % (sswfile, mech['mech_name'], mech['mech_code'])
            
            if mech['motive_type'] =='Q':
                self.location_map = translate.locations_quad
            else:
                self.location_map = translate.locations_biped
            
            try:
                mech_object = MechDesign.objects.get(ssw_filename=sswfile)            
            except MechDesign.DoesNotExist:
                mech_object = None
            
            mech_form = MechValidationForm(mech, instance=mech_object)
            
            if not mech_form.is_valid():
                raise SSWParseError(mech, mech_form.errors)
            
            mech_form.save()           
            
            mech_object = MechDesign.objects.get(ssw_filename=sswfile)
            mech_object.reset_equipment()
            
            locations = self.load_locations(mech, mech_object)
            
            self.load_equipment(mech, mech_object.id, mech.engine, locations)
            self.load_equipment(mech, mech_object.id, mech.armour, locations)        
            
            mech_form.save()
            transaction.commit()
        finally:
            transaction.rollback()
            