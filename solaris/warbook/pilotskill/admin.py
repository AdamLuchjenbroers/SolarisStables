from django.contrib import admin
from solaris.warbook.pilotskill import models

class PilotAbilityInline(admin.StackedInline):
    model = models.PilotAbility
    fields = ('name', 'description', 'bv_mod') 
    extra = 6
    max_num = 6
  
class PilotDisciplineAdmin(admin.ModelAdmin):
    inlines = [PilotAbilityInline,]
    
    
class PilotTraitAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return self.model.objects.filter(discipline=None)
    
    fields = ('name', 'description', ('bv_mod', 'trait_type'))
    
