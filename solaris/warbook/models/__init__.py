from types import ModuleType
from django.db.models.base import ModelBase
from sys import modules
from solaris.warbook.models import PilotAbilities, TechTree

models = modules[__name__]
moduleList = ['TechTree', 'PilotAbilities']
__all__ = []

for moduleName in moduleList:
  fullyQualifiedModuleName = '%s.%s' % (__name__, moduleName)
  moduleObj = modules[fullyQualifiedModuleName]
  
  __all__ += [item for item in dir(moduleObj) if isinstance(getattr(moduleObj, item), ModelBase)]
