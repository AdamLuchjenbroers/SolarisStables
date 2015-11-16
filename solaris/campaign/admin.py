from django.contrib import admin
from .models import Campaign, BroadcastWeek, Zodiac

class CampaignTechInline(admin.TabularInline):
    model = Campaign.initial_contracts.through

class CampaignAdmin(admin.ModelAdmin):
    inlines = [ CampaignTechInline ]
    exclude = ('initial_contracts',)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Zodiac)
admin.site.register(BroadcastWeek)
