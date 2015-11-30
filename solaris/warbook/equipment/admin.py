from django.contrib import admin
from django import forms

from solaris.warbook.equipment import models
from solaris.warbook.techtree.models import Technology

class EquipmentForm(forms.ModelForm):
    technology = forms.ModelMultipleChoiceField(
                   queryset = Technology.objects.all()
                 , label = 'Supplied By'
                 , widget = admin.widgets.FilteredSelectMultiple('Technologies', False)
                 )
    ammo_for = forms.ModelChoiceField(
                   queryset = models.Equipment.objects.filter(has_ammo=True)
                 , label = 'Ammunition For'
                 )

class HasTechnologyFilter(admin.SimpleListFilter):
    title = 'Has Technology'
    parameter_name = 'has_equip'

    def lookups(self, request, model_admin):
        return ( ('Y','Yes'), ('N','No') )

    def queryset(self, request, queryset):
        if self.value() == 'Y': 
            return queryset.filter(supplied_by__isnull=False).distinct()
        elif self.value() == 'N':
            return queryset.filter(supplied_by__isnull=True)
        else:
            return queryset
  
class EquipmentAdmin(admin.ModelAdmin):
    model = models.Equipment
    form = EquipmentForm
    list_filter = ('equipment_class', 'record_status', HasTechnologyFilter)
            
