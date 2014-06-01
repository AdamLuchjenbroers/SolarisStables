from django.contrib import admin
from django.db.models import Q
from solaris.warbook.pilotskill import models
    
class PilotTraitInline(admin.StackedInline):
    model = models.PilotTrait
    fields = ('name', 'description', 'bv_mod')  

class PilotAbilityInline(PilotTraitInline):
    extra = 6
    max_num = 6
  
class PilotDisciplineAdmin(admin.ModelAdmin):
    model = models.PilotDiscipline
    inlines = [PilotAbilityInline,]

    def queryset(self, request):
        return self.model.objects.filter(discipline_type='T')

class PilotTraitGroupAdmin(admin.ModelAdmin):
    model = models.PilotTraitGroup
    inlines = [PilotTraitInline,]
    
    def queryset(self, request):
        return self.model.objects.filter(~Q(discipline_type='T'))
    

    
