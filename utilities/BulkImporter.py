import os
import re


os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.dev_local'
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
            relative_path = relative_path + '/' + file
            loadMechDesign(fullpath, relative_path)
            

def loadMechDesign(sswFileName, sswRelName):
    sswData = SSWFile(sswFileName)
    
    if sswData.getTechBase() != 'Inner Sphere':
        return
    
    if sswData.getType() != 'BattleMech':
        return    
    
    print "Importing %s ( %s / %s )" % (sswRelName, sswData.getName(), sswData.getCode())
    MechDesign.objects.create(
                                mech_name = sswData.getName()
                              , mech_code = sswData.getCode()
                              , credit_value = sswData.getCost()
                              , bv_value = sswData.getBV()
                              , tonnage = sswData.getTonnage()
                              , move_walk = sswData.getWalkingMP()
                              , is_omni = sswData.isOmni()
                              , ssw_filename = sswRelName
                              )
    
if __name__ == '__main__':
    
    basepath = '/home/notavi/Programming/SourceData/SSW_Master'
    
    recursiveScanAll(basepath)
    
    