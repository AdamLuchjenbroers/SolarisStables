from django.db import models
from django.conf import settings

class CampaignManager(models.Manager):
    def get_current_campaign(self):
        return self.get(name=settings.CURRENT_CAMPAIGN)

class Campaign(models.Model):
    name = models.CharField(max_length=30)
    initial_balance = models.IntegerField()
    initial_contracts = models.ManyToManyField('warbook.Technology')

    objects = CampaignManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Campaign'
        db_table = 'campaign'
        app_label = 'campaign'

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()
    next = models.OneToOneField('Zodiac', related_name='prev', null=True)
    campaign = models.ForeignKey(Campaign, null=True, blank=True)

    class Meta:
        verbose_name = 'Zodiac Sign'
        db_table = 'campaign_zodiac'
        app_label = 'campaign'
    
    def __unicode__(self):
        return self.sign

class BroadcastWeekManager(models.Manager):
    def current_week(self):
        return super(BroadcastWeekManager,self).get(next_week=None)

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    next_week = models.OneToOneField('BroadcastWeek', null=True, blank=True, related_name='prev_week')
    campaign = models.ForeignKey(Campaign, null=True, blank=True)
  
    objects = BroadcastWeekManager()  

    def __unicode__(self):
        return 'Week %i' % self.week_number
        
    class Meta:
        verbose_name = 'Broadcast Week'
        db_table = 'campaign_broadcastweek'
        app_label = 'campaign'

    def advance(self):
        if self.next_week == None:            
            self.next_week = BroadcastWeek(
                week_number = self.week_number + 1
              , sign = self.sign.next
            )
            self.next_week.save()
            self.save()
        
        return self.next_week
    
