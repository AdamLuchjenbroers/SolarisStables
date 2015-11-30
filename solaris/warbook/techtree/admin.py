from django.contrib import admin
from solaris.warbook.techtree import models

class TechnologyRollModifierInline(admin.StackedInline):
    model = models.TechnologyRollModifier
    extra = 0

class TechnologyEquipmentInline(admin.TabularInline):
    model = models.Technology.access_to.through

  
class TechnologyAdmin(admin.ModelAdmin):
    fields = ['name', 'urlname', 'description', 'tier', 'category', 'base_difficulty', 'show']
    inlines = [TechnologyRollModifierInline,TechnologyEquipmentInline,]
