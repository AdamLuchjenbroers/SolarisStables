import os
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.dev_local'
from django.db import transaction

from solaris.utilities.forms import MechValidationForm
from solaris.utilities.parser import SSWFile
from solaris.warbook.mech import ref_data

sswPattern = re.compile('.*\.ssw$')

locations_all = {
	'hd': 'HD',
	'rt': 'RT',
	'rtr' : 'RRT',
	'lt' : 'LT',
	'ltr' : 'RLT',
	'ct' : 'CT',
	'ctr' : 'RCT',
	'ra' : 'RA',
	'la' : 'LA',
	'll' : 'LL',
	'rl' : 'RL',
}

locations_biped = locations_all.copy()
locations_biped['ra'] = 'RA'
locations_biped['la'] = 'LA'
locations_biped['ll'] = 'LL'
locations_biped['rl'] = 'RL'

locations_quad = locations_all.copy()
locations_quad['ra'] = 'RFL'
locations_quad['la'] = 'LFL'
locations_quad['ll'] = 'LRL'
locations_quad['rl'] = 'RRL'

def recursiveScanAll(path, relative_path='.'):
    
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            recursiveScanAll(fullpath, relative_path=relative_path + '/' + fileName)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            loadMechDesign(fullpath, relative_path  + '/' + fileName)

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
            
    
    
if __name__ == '__main__':
    
    basepath = '/home/notavi/Programming/SourceData/SSW_Master'
    
    recursiveScanAll(basepath)
    
    
