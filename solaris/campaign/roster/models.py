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
    group = models.ForeignKey(FightGroup)
    rules = MarkupField()
    is_simulation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Fight Types'
        verbose_name = 'Fight Type'
        db_table = 'campaign_fighttype'
        app_label = 'campaign'

class Map(models.Model):
    name = models.CharField(max_length=20)
    special_rules = MarkupField()

    class Meta:
        verbose_name_plural = 'Maps'
        verbose_name = 'Map'
        db_table = 'campaign_map'
        app_label = 'campaign'

class Condition(models.Model):
    name = models.CharField(max_length=20)
    rules = models.TextField()

    class Meta:
        verbose_name_plural = 'Conditions'
        verbose_name = 'Condition'
        db_table = 'campaign_conditions'
        app_label = 'campaign'

class RosteredFight(models.Model):
    week = models.ForeignKey(BroadcastWeek)
    fight_type = models.ForeignKey(FightType)
    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField(FightCondition)

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'campaign_rosteredfight'
        app_label = 'campaign'
