from django.db import models

from markitup.fields import MarkupField

from solaris.campaign.models import BroadcastWeek

class FightGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Fight Groups'
        verbose_name = 'Fight Group'
        db_table = 'campaign_fightgroup'
        app_label = 'campaign'
    
class FightType(models.Model):
    group = models.ForeignKey('campaign.FightGroup')
    name = models.CharField(max_length=50)
    rules = MarkupField(blank=True)
    is_simulation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Fight Types'
        verbose_name = 'Fight Type'
        db_table = 'campaign_fighttype'
        app_label = 'campaign'

class Map(models.Model):
    name = models.CharField(max_length=20)
    special_rules = MarkupField(blank=True)

    class Meta:
        verbose_name_plural = 'Maps'
        verbose_name = 'Map'
        db_table = 'campaign_map'
        app_label = 'campaign'

class FightCondition(models.Model):
    name = models.CharField(max_length=20)
    rules = MarkupField()

    class Meta:
        verbose_name_plural = 'Fight Conditions'
        verbose_name = 'Fight Condition'
        db_table = 'campaign_conditions'
        app_label = 'campaign'

class RosteredFightCondition(models.Model):
    fight = models.ForeignKey('campaign.RosteredFight')
    condition = models.ForeignKey('campaign.FightCondition')
    annotation = models.CharField(max_length=20, blank=True)

class RosteredFight(models.Model):
    week = models.ForeignKey('campaign.BroadcastWeek', related_name='fights')
    fight_type = models.ForeignKey('campaign.FightType')
    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField(FightCondition, through=RosteredFightCondition)

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'campaign_rosteredfight'
        app_label = 'campaign'
