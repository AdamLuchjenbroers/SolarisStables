from django.contrib import admin
from solaris.warbook import models

class TechnologyRollModifierInline(admin.StackedInline):
  model = models.TechnologyRollModifier
  extra = 0
  
class TechnologyAdmin(admin.ModelAdmin):
  fields = ['name', 'urlname', 'description', 'tier', 'category', 'base_difficulty', 'show']
  inlines = [TechnologyRollModifierInline,]

class PilotAbilityInline(admin.StackedInline):
  model = models.PilotAbility
  extra = 6
  
class PilotDisciplineAdmin(admin.ModelAdmin):
  inlines = [PilotAbilityInline,]

admin.site.register(models.Technology, TechnologyAdmin)
admin.site.register(models.PilotDiscipline, PilotDisciplineAdmin)


