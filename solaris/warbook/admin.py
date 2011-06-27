from django.contrib import admin
from solaris.warbook import models

class TechnologyRoleModifierInline(admin.StackedInline):
  model = models.TechnologyRoleModifier
  extra = 0
  
class TechnologyAdmin(admin.ModelAdmin):
  fields = ['name', 'urlname', 'description', 'tier', 'base_difficulty', 'show']
  inlines = [TechnologyRoleModifierInline]

admin.site.register(models.Technology, TechnologyAdmin)