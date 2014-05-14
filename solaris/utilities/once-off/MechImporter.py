import os
import re

from django.conf import settings

from solaris.utilities.loader import MechLoader

sswPattern = re.compile('.*\.ssw$')

def recursiveScanAll(path, relative_path='.'):
   
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            recursiveScanAll(fullpath, relative_path=relative_path + '/' + fileName)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            loader = MechLoader()
            loader.load_mech(relative_path  + '/' + fileName)   
    
if __name__ == '__main__':
    
    basepath = settings.SSW_STOCK_MECHS_ROOT
        
    recursiveScanAll(basepath)
    
    
