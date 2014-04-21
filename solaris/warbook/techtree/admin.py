from django.contrib import admin
from solaris.warbook.techtree import models

class TechnologyRollModifierInline(admin.StackedInline):
    model = models.TechnologyRollModifier
    extra = 0
  
class TechnologyAdmin(admin.ModelAdmin):
    fields = ['name', 'urlname', 'description', 'tier', 'category', 'base_difficulty', 'show']
    inlines = [TechnologyRollModifierInline,]