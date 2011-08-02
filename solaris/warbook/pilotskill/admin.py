from django.contrib import admin
from solaris.warbook.pilotskill import models

class PilotAbilityInline(admin.StackedInline):
  model = models.PilotAbilities.PilotAbility
  extra = 6
  
class PilotDisciplineAdmin(admin.ModelAdmin):
  inlines = [PilotAbilityInline,]


admin.site.register(models.PilotDiscipline, PilotDisciplineAdmin)


