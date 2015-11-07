from django.contrib import admin
from solaris.stablemanager import models
from solaris.stablemanager.mechs import models as asset_models

#admin.site.register(models.Mech)
admin.site.register(models.Stable)
admin.site.register(asset_models.StableMech)
admin.site.register(asset_models.Pilot)
