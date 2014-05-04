import os
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'solaris.settings.dev_local'
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError, DatabaseError
from django.forms.models import model_to_dict

from solaris.warbook.mech.models import MechDesign
from solaris.warbook.mech.forms import MechValidationForm


sswPattern = re.compile('.*\.ssw$')

from utilities.Skunkwerks import SSWFile

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
    
    if sswData.getTechBase() != 'Inner Sphere':
        transaction.rollback() # Roll it back even though nothing has happened to fix errors regarding uncommitted transactions.
        return
    
    if sswData.getType() != 'BattleMech':
        transaction.rollback() # Roll it back even though nothing has happened to fix errors regarding uncommitted transactions.
        return    
    
    print "Importing %s ( %s / %s )" % (sswRelName, sswData.getName(), sswData.getCode())
    # Try to retrieve the existing mech entry, but if not found then 
    # create a new one.
    try:
        mech_object = MechDesign.objects.get(ssw_filename=sswRelName)
        mech_dict = model_to_dict(mech_object)
    except ObjectDoesNotExist:
        mech_object = MechDesign()
        mech_dict = {}
        mech_dict['ssw_filename'] = sswRelName
    except DatabaseError as e:
        print 'Error encountered reading from database: %s' % e.message
        transaction.rollback()
        return
    
        
    mech_dict['mech_name'] = sswData.getName()
    mech_dict['mech_code'] = sswData.getCode()
    mech_dict['credit_value'] = sswData.getCost()
    mech_dict['bv_value'] = sswData.getBV()
    mech_dict['tonnage'] = sswData.getTonnage()
    mech_dict['engine_rating'] = sswData.getEngineRating()
    mech_dict['is_omni'] = sswData.isOmni()
    
    mech = MechValidationForm(mech_dict, instance=mech_object)
    
    if mech.is_valid():
        mech.save()
        transaction.commit()
    else:
        print 'Unable to save %s %s (file: %s)' % (mech_dict['mech_name'], mech_dict['mech_code'], mech_dict['ssw_filename'])
        for err in mech.errors:
            print '\t* %s' % err.message
        transaction.rollback()
    
if __name__ == '__main__':
    
    basepath = '/home/notavi/Programming/SourceData/SSW_Master'
    
    recursiveScanAll(basepath)
    
    