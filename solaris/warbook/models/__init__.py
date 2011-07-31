from types import ModuleType
from django.db.models.base import ModelBase
from sys import modules

moduleList = ['TechTree', 'PilotAbilities']
__all__ = []

for moduleName in moduleList:
  fullyQualifiedModuleName = '%s.%s' % (__name__, moduleName)
  moduleObj = __import__(fullyQualifiedModuleName)
  
  __all__ += [item for item in dir(moduleObj) if isinstance(getattr(moduleObj, item), ModelBase)]
