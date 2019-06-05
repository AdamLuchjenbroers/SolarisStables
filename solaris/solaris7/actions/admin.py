from django.contrib import admin
from django import forms

from . import models

class ActionGroupForm(forms.ModelForm):
    class Meta:
        model = models.ActionGroup
        fields = ('group', 'description', 'start_only')
    
        labels = {
          'group' : 'Group Name'
        , 'start_only' : 'Beginning of Week Only'
        , 'description' : 'Description'
        } 

class ActionTypeForm(forms.ModelForm):
    class Meta:
        model = models.ActionType
        fields = ('group', 'action', 'max_per_week', 'base_cost', 'base_cost_max', 'description')
    
        labels = {
          'group' : 'Group'
        , 'action' : 'Action'
        , 'description' : 'Description'
        , 'max_per_week' : 'Max Per Week'
        , 'base_cost' : 'Cost'
        , 'base_cost_max' : 'Max Cost'
        } 


class ActionGroupAdmin(admin.ModelAdmin):
    model = models.ActionGroup
    form = ActionGroupForm
    fields = (('group', 'start_only'), 'description')

class ActionTypeAdmin(admin.ModelAdmin):
    model = models.ActionType
    form = ActionTypeForm
    fields = (('group', 'action', 'max_per_week'), ('base_cost', 'base_cost_max'), 'description')


