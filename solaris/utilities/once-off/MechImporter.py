import os
import re

from django.conf import settings

from solaris.utilities.loader import MechLoader

sswPattern = re.compile('.*\.ssw$')

failures = {}

def recursiveScanAll(path, relative_path='.'):
   
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            recursiveScanAll(fullpath, relative_path=relative_path + '/' + fileName)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            try: 
                loader = MechLoader()
                loader.load_mech(relative_path  + '/' + fileName)
            except Error as e:
                failures[relative_path] = e   
    
if __name__ == '__main__':
    
    basepath = settings.SSW_STOCK_MECHS_ROOT
        
    recursiveScanAll(basepath)
    
    for file, errors in failures.keys():
        print 'Errors encountered processing %s' % file
        
        for err in errors:
            print '\t%s' % err.value
    
    
