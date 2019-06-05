from django.contrib import admin
from django import forms
from . import models

import solaris.solaris7.fightinfo.models as fight_models
import solaris.solaris7.fightinfo.admin as fight_admin

import solaris.solaris7.actions.models as action_models
import solaris.solaris7.actions.admin as action_admin

class SolarisCampaignTechInline(admin.TabularInline):
    model = models.SolarisCampaign.initial_contracts.through

class SolarisCampaignPilotTemplateInline(admin.StackedInline):
    model = models.StartingPilotTemplate
    fields= (('count', 'rank', 'piloting', 'gunnery', 'fame'),)

class SolarisCampaignAdminForm(forms.ModelForm):
    class Meta:
      models = models.SolarisCampaign
      fields = ('name', 'initial_balance', ('actions_startweek', 'actions_duringweek')) 

      labels = {
        'name' : 'Campaign Name'
      , 'initial_balance' : 'Starting C-Bills'
      , 'actions_startweek' : 'Actions (Start of Week)'
      , 'actions_duringweek' : 'Actions (During Week)'
      }

class SolarisCampaignAdmin(admin.ModelAdmin):
    inlines = [ SolarisCampaignTechInline, SolarisCampaignPilotTemplateInline ]
    fields = ('name', 'initial_balance', ('actions_startweek', 'actions_duringweek')) 
    form = SolarisCampaignAdminForm

admin.site.register(models.SolarisCampaign, SolarisCampaignAdmin)
admin.site.register(models.Zodiac)
admin.site.register(models.BroadcastWeek)

# Import Fight Types
admin.site.register(fight_models.FightGroup, fight_admin.FightGroupAdmin)
admin.site.register(fight_models.FightCondition)

admin.site.register(fight_models.Map)

# Import Actions
admin.site.register(action_models.ActionGroup, action_admin.ActionGroupAdmin)
admin.site.register(action_models.ActionType, action_admin.ActionTypeAdmin)
