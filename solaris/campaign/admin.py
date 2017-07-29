from django.contrib import admin
from . import models 

class CampaignTechInline(admin.TabularInline):
    model = models.Campaign.initial_contracts.through

class CampaignPilotTemplateInline(admin.StackedInline):
    model = models.StartingPilotTemplate
    fields= (('count', 'rank', 'piloting', 'gunnery', 'fame'),)

class CampaignAdmin(admin.ModelAdmin):
    inlines = [ CampaignTechInline, CampaignPilotTemplateInline ]
    exclude = ('initial_contracts',)

admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Zodiac)
admin.site.register(models.BroadcastWeek)
