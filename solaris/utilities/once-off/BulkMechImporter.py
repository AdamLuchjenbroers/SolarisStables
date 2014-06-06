import os
import re
import traceback

from django.conf import settings

from solaris.utilities.loader import SSWLoader

sswPattern = re.compile('.*\.ssw$')

failures = {}

def recursiveScanAll(path, relative_path='.'):
   
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            recursiveScanAll(fullpath, relative_path=relative_path + '/' + fileName)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            try: 
                loader = SSWLoader(relative_path  + '/' + fileName)
                loader.load_mechs()
            except BaseException as e:
                print '%s > %s ' % (relative_path, e)
                traceback.print_exc()
                failures[relative_path] = e
            finally:
                #Explicitly free memory, because letting them pile up is a serious memory hog
                del loader   
    
if __name__ == '__main__':
    
    basepath = settings.SSW_STOCK_MECHS_ROOT
        
    recursiveScanAll(basepath)
    
    for file, errors in failures.items():
        print 'Errors encountered processing %s' % file
        
        for err in errors:
            print '\t%s' % err
    
    