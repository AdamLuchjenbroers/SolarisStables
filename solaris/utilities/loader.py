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

class SSWLoader(object):

    def __init__(self, sswfile, basepath=settings.SSW_STOCK_MECHS_ROOT):
        self.xml_fd = open('%s/%s' % (basepath, sswfile),'rb')
            
        self.filename = sswfile            
        self.sswXML = etree.parse(self.xml_fd)

    def get_model_details(self):
        result = {
          'mech_name' : self.sswXML.xpath('/mech/@name')[0]
        , 'mech_code' : self.sswXML.xpath('/mech/@model')[0]
        , 'is_omni'   : self.sswXML.xpath('/mech/@omnimech')[0] == 'TRUE'
        , 'tons'      : int(self.sswXML.xpath('/mech/@tons')[0])
        , 'cost'      : float(self.sswXML.xpath('/mech/cost/text()')[0])
        , 'motive_type' : self.sswXML.xpath('/mech/motive_type/text()')[0]
        , 'techbase'  : self.sswXML.xpath('/mech/techbase/text()')[0]
        }

        if result['is_omni'] == False:
	   result['bv'] = int(self.sswXML.xpath('/mech/battle_value/text()')[0])
        else:
           result['bv'] = None

           config_list={}
           for config in self.sswXML.xpath('/mech/loadout'):
               config_name = config.get('name')
               config_data = {
                 'bv'   : int(config.xpath('./battle_value/text()')[0])
               , 'cost' : float(config.xpath('./cost/text()')[0])
               }

               config_list[config_name] = config_data

           result['loadouts'] = config_list

        return result;
    
    def load_single_loadout(self, loadout_name, basechassis, production_type='P', print_message=True):
        parsed_mechs = SSWMech( self.sswXML.xpath('/mech')[0], self.filename, production_type=production_type )
        
        loadout = parsed_mechs.get_loadout(loadout_name)
        if loadout != None:
            loadout_mech = MechLoader(self.filename, loadout)
            loadout_mech.parsed_mech['omni_basechassis'] = basechassis.id
            loadout_mech.load_mech()            
            return loadout_mech.mech
        else:
            return None

    def load_mechs(self, production_type='P', print_message=True):
        parsed_mechs = SSWMech( self.sswXML.xpath('/mech')[0], self.filename, production_type=production_type )
            
        if parsed_mechs.type != 'BattleMech' or parsed_mechs['tech_base'] != 'I' or int(parsed_mechs['tonnage']) < 20:
            return 
        
        if print_message:
            print "Importing %s ( %s / %s )" % (self.filename, parsed_mechs['mech_name'], parsed_mechs['mech_code'])
        
        # Load Base Config
        base_config = MechLoader(self.filename, parsed_mechs)
        base_config.load_mech()
        
        for loadout in parsed_mechs.loadouts:
            if print_message:
                print " * Importing Config: %s" % loadout['omni_loadout']
            loadout_mech = MechLoader(self.filename, loadout)
            loadout_mech.parsed_mech['omni_basechassis'] = base_config.mech.id
            loadout_mech.load_mech()
            
        
class MechLoader(object):
 
    def __init__(self, sswfile, parsed_mech):
        self.parsed_mech = parsed_mech
        self.filename = sswfile            
        self.locations = None 
 
        try:
            self.mech = MechDesign.objects.get(ssw_filename=self.filename, omni_loadout=parsed_mech['omni_loadout'])            
        except MechDesign.DoesNotExist:
            self.mech = None
    

    def exists(self):
        return (self.mech != None)
    
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
    
    def load_equipment(self, equipment):
        equipment['mech'] = self.mech.id
        
        if equipment.equipment.critical_func:
            equipment.extrapolate(equipment.equipment.criticals(mech=self.mech))
        
        eq_form = MechEquipmentForm(equipment)
                
        if eq_form.is_valid():
            eq_form.save()
                    
            for ssw_loc, mount in equipment.mountings.items():
                loc_code = self.location_map[ssw_loc]
                
                mount['equipment'] = eq_form.instance.id
                mount['location'] = self.location_models[loc_code].id
                mount_form = MountingForm(mount)
                if mount_form.is_valid():
                    mount_form.save()
                else:
                    raise SSWParseError(self.filename, mount_form.errors)
            eq_form.save()
        else:
            raise SSWParseError(self.filename, eq_form.errors)
                
    @transaction.atomic
    def load_mech(self):
        self.location_models = None

        try:
            if self.parsed_mech['motive_type'] =='Q':
                self.location_map = translate.locations_quad
            else:
                self.location_map = translate.locations_biped
 
            mech_form = MechValidationForm(self.parsed_mech, instance=self.mech)            
            if not mech_form.is_valid():
                raise SSWParseError(self.parsed_mech, mech_form.errors)
            
            mech_form.save()           
            
            self.mech = mech_form.instance
            self.mech.reset_equipment()
            
            self.location_models = self.load_locations(self.parsed_mech, self.mech)
            
            lazy_evaluation = []
            
            for gear in self.parsed_mech.equipment:
                if gear.equipment.evaluate_last:
                    lazy_evaluation.append(gear)
                else:
                    self.load_equipment(gear)
                    
            for gear in lazy_evaluation:
                self.load_equipment(gear)
            
            mech_form.save()
            self.mech.update_required_techs()
            self.mech.refresh_tier()
        finally:
            #Free Resources
            if self.parsed_mech:
                del self.parsed_mech
            
            if self.location_models:
                del self.location_models 
