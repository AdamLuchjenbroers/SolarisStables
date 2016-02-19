from django.contrib import admin
from solaris.warbook.techtree import models

class TechnologyRollModifierInline(admin.StackedInline):
    model = models.TechnologyRollModifier
    extra = 0

class HasEquipmentFilter(admin.SimpleListFilter):
    title = 'Has Equipment'
    parameter_name = 'has_equip'

    def lookups(self, request, model_admin):
        return ( ('Y','Yes'), ('N','No') )

    def queryset(self, request, queryset):
        if self.value() == 'Y': 
            return queryset.filter(access_to__isnull=False).distinct()
        elif self.value() == 'N':
            return queryset.filter(access_to__isnull=True)
        else:
            return queryset
  
class TechnologyAdmin(admin.ModelAdmin):
    fields = ['name', 'urlname', 'description', 'tier', 'base_difficulty', 'show', 'access_to']
    filter_horizontal = ('access_to',)
    inlines = [TechnologyRollModifierInline,]
    list_filter = ('tier', HasEquipmentFilter )
