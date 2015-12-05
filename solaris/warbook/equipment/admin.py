from django.contrib import admin
from django import forms

from solaris.warbook.equipment import models
from solaris.warbook.techtree.models import Technology

class EquipmentForm(forms.ModelForm):
    supplied_by = forms.ModelMultipleChoiceField(
                   queryset = Technology.objects.all()
                 , label = 'Supplied By'
                 , widget = admin.widgets.FilteredSelectMultiple('Technologies', False)
                 , required = False
                 )
    ammo_for = forms.ModelChoiceField(
                 queryset = models.Equipment.objects.filter(has_ammo=True)
               , label = 'Ammunition For'
               , required = False
               )

    class Meta:
        model = models.Equipment
        fields = ('name', 'equipment_class', 'ssw_name', 'tonnage_func','tonnage_factor', 'critical_func', 'critical_factor'
                 , 'cost_func', 'cost_factor', 'splittable', 'crittable', 'has_ammo', 'ammo_for','ammo_size', 'basic_ammo'
                 , 'weapon_properties', 'evaluate_last', 'fcs_artemis_iv', 'fcs_artemis_v', 'fcs_apollo', 'supplied_by'
                 , 'record_status')
        labels = {
          'ssw_name' : 'Skunkwerks Name'
        , 'tonnage_func' : 'Tonnage Formula'
        , 'tonnage_factor' : 'Tonnage Factor'
        , 'critical_func' : 'Criticals Formula'
        , 'critical_factor' : 'Criticals Factor'
        , 'cost_func' : 'Cost Formula'
        , 'cost_factor' : 'Cost Factor'
        , 'fcs_artemis_iv' : 'Supports Artemis IV'
        , 'fcs_artemis_v' : 'Supports Artemis V'
        , 'fcs_apollo' : 'Supports Apollo'
        } 

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

    readonly_fields = ('ssw_name',)
    fields = ( 'ssw_name'
             , ('name', 'equipment_class')
             , ('tonnage_func','tonnage_factor')
             , ('critical_func', 'critical_factor')
             , ('cost_func', 'cost_factor')
             , ('splittable', 'crittable')
             , ('has_ammo', 'ammo_for','ammo_size', 'basic_ammo')
             , 'weapon_properties'
             , 'evaluate_last'
             , ('fcs_artemis_iv', 'fcs_artemis_v', 'fcs_apollo')
             , 'supplied_by'
             , 'record_status'
             ) 
            
