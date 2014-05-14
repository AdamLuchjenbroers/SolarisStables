from lxml import etree

from django.conf import settings
from django.db import transaction

from .parser import SSWMech
from .forms import MechValidationForm

@transaction.commit_manually
def parse(sswfile):
    filename = '%s/%s' % (settings.SSW_STOCK_MECHS_ROOT, sswfile)
    fd = open(filename,'rb')
    
    sswXML = etree.parse(fd)
    mech = SSWMech( sswXML.xpath('/mech')[0], sswfile )
    
    mech_form = MechValidationForm(mech)
    if mech_form.is_valid():
        mech_form.save()
        transaction.commit()
    else:
        transaction.rollback()
