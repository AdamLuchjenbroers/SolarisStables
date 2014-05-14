from lxml import etree

from django.conf import settings
from django.db import transaction

from .parser import SSWMech
from .forms import MechValidationForm

@transaction.commit_manually
def load_mech(sswfile):
    filename = '%s/%s' % (settings.SSW_STOCK_MECHS_ROOT, sswfile)
    fd = open(filename,'rb')
    
    sswXML = etree.parse(fd)
    mech = SSWMech( sswXML.xpath('/mech')[0], sswfile )

    print "Importing %s ( %s / %s )" % (sswfile, mech['mech_name'], mech['mech_code'])
    
    mech_form = MechValidationForm(mech)
    if mech_form.is_valid():
        mech_form.save()
        transaction.commit()
    else:
        transaction.rollback()


@transaction.commit_manually           
def loadMechDesign(sswFileName, sswRelName):
    sswData = SSWFile(sswFileName)
    
    if sswData.get_techbase() != 'Inner Sphere':
        transaction.rollback() # Roll it back even though nothing has happened to fix errors regarding uncommitted transactions.
        return
    
    if sswData.get_type() != 'BattleMech':
        transaction.rollback() # Roll it back even though nothing has happened to fix errors regarding uncommitted transactions.
        return    
    
    print "Importing %s ( %s / %s )" % (sswRelName, sswData.getName(), sswData.getCode())
    # Try to retrieve the existing mech entry, but if not found then 
    # create a new one.
     
    mech = MechValidationForm.load_from_xml(sswFileName, sswRelName)
    
    if mech.is_valid():
        mech.save()
        transaction.commit()
    else:
        transaction.rollback()
        print 'Import failed from file: %s' % (sswRelName)
        for (field, error) in mech.errors.items():
            print '\t* %s: %s' % (field, error)
            