from django.contrib import admin
from solaris.warbook import models

class TechnologyRollModifierInline(admin.StackedInline):
  model = models.TechTree.TechnologyRollModifier
  extra = 0
  
class TechnologyAdmin(admin.ModelAdmin):
  fields = ['name', 'urlname', 'description', 'tier', 'category', 'base_difficulty', 'show']
  inlines = [TechnologyRollModifierInline,]

class PilotAbilityInline(admin.StackedInline):
  model = models.PilotAbilities.PilotAbility
  extra = 6
  
class PilotDisciplineAdmin(admin.ModelAdmin):
  inlines = [PilotAbilityInline,]

admin.site.register(models.TechTree.Technology, TechnologyAdmin)
admin.site.register(models.PilotAbilities.PilotDiscipline, PilotDisciplineAdmin)


