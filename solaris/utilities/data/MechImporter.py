#!/usr/bin/python2.7
import sys
import traceback

from django.conf import settings

from solaris.utilities.loader import SSWLoader


if __name__ == '__main__':
    ssw_file = sys.argv[1]

    try: 
        loader = SSWLoader(ssw_file)
        loader.load_mechs()
        del loader   
    except BaseException as e:
        print '%s > %s ' % (ssw_file, e)
        traceback.print_exc()
