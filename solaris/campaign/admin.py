from django.contrib import admin
from django import forms
from . import models

class CampaignAdminForm(forms.ModelForm):
    class Meta:
      models = models.Campaign

class CampaignAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Campaign, CampaignAdmin)
