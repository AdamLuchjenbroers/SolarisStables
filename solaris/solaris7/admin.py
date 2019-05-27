from django.contrib import admin
from django import forms
from . import models

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
