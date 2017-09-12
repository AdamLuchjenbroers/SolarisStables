from django.contrib import admin
from django import forms
from . import models 

class CampaignTechInline(admin.TabularInline):
    model = models.Campaign.initial_contracts.through

class CampaignPilotTemplateInline(admin.StackedInline):
    model = models.StartingPilotTemplate
    fields= (('count', 'rank', 'piloting', 'gunnery', 'fame'),)

class CampaignAdminForm(forms.ModelForm):
    class Meta:
      models = models.Campaign
      fields = ('name', 'initial_balance', ('actions_startweek', 'actions_duringweek')) 

      labels = {
        'name' : 'Campaign Name'
      , 'initial_balance' : 'Starting C-Bills'
      , 'actions_startweek' : 'Actions (Start of Week)'
      , 'actions_duringweek' : 'Actions (During Week)'
      }

class CampaignAdmin(admin.ModelAdmin):
    inlines = [ CampaignTechInline, CampaignPilotTemplateInline ]
    fields = ('name', 'initial_balance', ('actions_startweek', 'actions_duringweek')) 
    form = CampaignAdminForm

admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Zodiac)
admin.site.register(models.BroadcastWeek)
