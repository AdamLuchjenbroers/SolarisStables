from django.contrib import admin
from solaris.stablemanager import models
from solaris.stablemanager.mechs import models as mech_models
from solaris.stablemanager.pilots import models as pilot_models

#admin.site.register(models.Mech)
admin.site.register(models.Stable)
admin.site.register(mech_models.StableMech)
admin.site.register(pilot_models.Pilot)
