from django.db import models

from markitup.fields import MarkupField

from solaris.campaign.models import BroadcastWeek

class RosteredFightCondition(models.Model):
    fight = models.ForeignKey('campaign.RosteredFight')
    condition = models.ForeignKey('warbook.FightCondition')
    annotation = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        if self.annotation not in (None, ''):
            return '%s (%s)' % (self.condition.name, self.annotation)
        else:
            return self.condition.name

    class Meta:
        db_table = 'campaign_fight_x_condition'
        app_label = 'campaign'

class RosteredFight(models.Model):
    week = models.ForeignKey('campaign.BroadcastWeek', related_name='fights')
    fight_type = models.ForeignKey('warbook.FightType')
    fight_map = models.ForeignKey('warbook.Map')
    purse = models.IntegerField(blank=True, null=True)
    units = models.IntegerField(default=1)
    
    # For Omnimech fights and special challenges
    chassis = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    tonnage = models.IntegerField(null=True, blank=True)
    weightclass = models.ForeignKey('warbook.WeightClass', null=True, blank=True)

    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField('warbook.FightCondition', through=RosteredFightCondition)

    def weightclass_text(self):
        if self.units == 1:
            if self.chassis != None:
               return self.chassis
            elif self.weightclass != None:
               return self.weightclass
        
        if self.tonnage != None:
            return '%i Tons'
        else:
            return ''

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'campaign_rosteredfight'
        app_label = 'campaign'
        ordering = ['fight_type__order', 'units', 'weightclass__lower', 'tonnage']
