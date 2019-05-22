from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class CampaignManager(models.Manager):
    def get_current_campaign(self):
        return self.get(name=settings.CURRENT_CAMPAIGN)

class Campaign(models.Model):
    name = models.CharField(max_length=30)

    objects = CampaignManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Campaign'
        db_table = 'campaign'
        app_label = 'campaign'
