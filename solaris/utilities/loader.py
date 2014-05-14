from lxml import etree

from django.conf import settings
from django.db import transaction
from django.utils.html import strip_tags

from solaris.warbook.mech.models import MechDesign

from .parser import SSWMech
from .forms import MechValidationForm

def print_errors(errors):
    for (key, value) in errors.items():
        print '\t%s: %s' % (key, strip_tags('%s' % value))

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
        
        mech_form.save()
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise e
            