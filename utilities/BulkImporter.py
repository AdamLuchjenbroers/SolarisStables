import os
import re


os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.dev_local'
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from solaris.warbook.mech.models import MechDesign


sswPattern = re.compile('.*\.ssw$')

from utilities.Skunkwerks import SSWFile


def recursiveScanAll(path, relative_path='.'):
    for file in os.listdir(path):
        fullpath = path + '/' + file
        
        if os.path.isdir(fullpath):
            relative_path = relative_path + '/' + file
            recursiveScanAll(fullpath, relative_path=relative_path)
            
        if os.path.isfile(fullpath) and sswPattern.match(file):
            loadMechDesign(fullpath, relative_path  + '/' + file)
            

def loadMechDesign(sswFileName, sswRelName):
    sswData = SSWFile(sswFileName)
    
    if sswData.getTechBase() != 'Inner Sphere':
        return
    
    if sswData.getType() != 'BattleMech':
        return    
    
    print "Importing %s ( %s / %s )" % (sswRelName, sswData.getName(), sswData.getCode())
    # Try to retrieve the existing mech entry, but if not found then 
    # create a new one.
    try:
        mechDB = MechDesign.objects.get(ssw_filename=sswRelName)
    except ObjectDoesNotExist:
        mechDB = MechDesign()
        mechDB.ssw_filename = sswRelName
        
    mechDB.mech_name = sswData.getName()
    mechDB.mech_code = sswData.getCode()
    mechDB.credit_value = sswData.getCost()
    mechDB.bv_value = sswData.getBV()
    mechDB.tonnage = sswData.getTonnage()
    mechDB.move_walk = sswData.getWalkingMP()
    mechDB.is_omni = sswData.isOmni()
    
    try:
        mechDB.save()
    except IntegrityError:
        print 'Unable to import %s %s (File: %s). Already loaded from another file.' % (sswData.getName(), sswData.getCode(), sswRelName)
    
if __name__ == '__main__':
    
    basepath = '/home/notavi/Programming/SourceData/SSW_Master'
    
    recursiveScanAll(basepath)
    
    