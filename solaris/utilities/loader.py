from lxml import etree

from django.conf import settings
from django.db import transaction
from django.utils.html import strip_tags

from solaris.warbook.mech.models import MechDesign, MechLocation, MechDesignLocation
from solaris.utilities import translate

from .parser import SSWMech
from .forms import MechValidationForm, LocationValidationForm

def print_errors(errors):
    for (key, value) in errors.items():
        print '\t%s: %s' % (key, strip_tags('%s' % value))

def load_locations(mech, mech_model):
    for (loc_code, armour) in mech.armour.armour.items():
        loc_xlat = translate.locations_all[loc_code]
        loc_model = MechLocation.objects.get(location=loc_xlat)
        
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
            print_errors(form.errors)
        
            
@transaction.commit_manually
def load_mech(sswfile):
    try:
        filename = '%s/%s' % (settings.SSW_STOCK_MECHS_ROOT, sswfile)
        fd = open(filename,'rb')
        
        sswXML = etree.parse(fd)
        mech = SSWMech( sswXML.xpath('/mech')[0], sswfile )
        
        if mech.type != 'BattleMech' or mech['tech_base'] != 'I':
            transaction.rollback()
            return 
        
        print "Importing %s ( %s / %s )" % (sswfile, mech['mech_name'], mech['mech_code'])
        
        try:
            mech_object = MechDesign.objects.get(ssw_filename=sswfile)            
        except MechDesign.DoesNotExist:
            mech_object = None
        
        mech_form = MechValidationForm(mech, instance=mech_object)
        if not mech_form.is_valid():
            print_errors(mech_form.errors)
            transaction.rollback()
            return
        
        mech_object = MechDesign.objects.get(ssw_filename=sswfile)
        
        load_locations(mech, mech_object)           
        
        mech_form.save()
        transaction.commit()
    except Exception as e:
        print e
        transaction.rollback()
        raise e
            