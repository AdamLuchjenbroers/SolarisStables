#!/home/notavi/Programming/Solaris/bin/python2.7

# Recommended Manage.py for Django 1.4+
#    https://docs.djangoproject.com/en/1.4/releases/1.4/#updated-default-project-layout-and-manage-py

from os import environ

import sys

if __name__ == "__main__":
    environ.setdefault("DJANGO_SETTINGS_MODULE", environ['DJANGO_SETTINGS_MODULE'])
    
    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)
    
