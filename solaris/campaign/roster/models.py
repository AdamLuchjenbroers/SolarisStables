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
    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField('warbook.FightCondition', through=RosteredFightCondition)
    order = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'campaign_rosteredfight'
        app_label = 'campaign'
