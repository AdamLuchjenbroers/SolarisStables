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
  
class EquipmentAdmin(admin.ModelAdmin):
    model = models.Equipment
    form = EquipmentForm
    list_filter = ('equipment_class', 'record_status')
            
