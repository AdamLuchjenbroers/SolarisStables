import os
import re
import traceback

from django.conf import settings

from solaris.utilities.loader import SSWLoader

sswPattern = re.compile('.*\.ssw$')

def loadMechFolder(path=settings.SSW_STOCK_MECHS_ROOT, relative_path='.', basepath=None):
    failures = {}
    
    if basepath == None:
        #We're the first call
        basepath = path
       
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            loadMechFolder(path=fullpath, relative_path=relative_path + '/' + fileName, basepath=basepath)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            try: 
                loader = SSWLoader(relative_path + '/' + fileName, basepath=basepath)
                loader.load_mechs()
            except BaseException as e:
                print '%s > %s ' % (relative_path, e)
                traceback.print_exc()
                failures[fullpath] = e
            finally:
                #Explicitly free memory, because letting them pile up is a serious memory hog
                del loader   
        
    for fileName, errors in failures.items():
        print 'Errors encountered processing %s' % fileName
        
        for err in errors:
            print '\t%s' % err
    

    
