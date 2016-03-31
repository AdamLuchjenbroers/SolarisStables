from django.contrib import admin
from django.db.models import Q
from solaris.warbook.pilotskill import models
    
class PilotTraitInline(admin.StackedInline):
    model = models.PilotTrait
    fields = (('name', 'table', 'item'), 'description', 'bv_mod')  

class PilotTraitGroupAdmin(admin.ModelAdmin):
    model = models.PilotTraitGroup
    inlines = [PilotTraitInline,]

    

    
