from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils.text import slugify

class CampaignManager(models.Manager):
    def get_current_campaign(self):
        return self.get(name=settings.CURRENT_CAMPAIGN)

class Campaign(models.Model):
    name = models.CharField(max_length=30)
    urlname = models.CharField(max_length=30, unique=True) 

    campaign_states = (
      ('P', 'Preparation')
    , ('A', 'Active')
    , ('C', 'Complete')
    )
    campaign_state = models.CharField(max_length=1, choices=campaign_states, default='P')

    invite_only = models.BooleanField(default=True)

    objects = CampaignManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.urlname == None:
            self.urlname = slugify(unicode(self.name))

        super(FightType, self).save()

    class Meta:
        verbose_name = 'Campaign'
        db_table = 'campaign'
        app_label = 'campaign'
