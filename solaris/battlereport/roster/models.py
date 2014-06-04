from django.db import models

from markitup.fields import MarkupField

from solaris.battlereport.models import BroadcastWeek

class FightGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Fight Groups'
        verbose_name = 'Fight Group'
        db_table = 'battlereport_fightgroup'
        app_label = 'battlereport'
    
class FightType(models.Model):
    group = models.ForeignKey(FightGroup)
    rules = MarkupField()
    is_simulation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Fight Types'
        verbose_name = 'Fight Type'
        db_table = 'battlereport_fighttype'
        app_label = 'battlereport'

class Map(models.Model):
    name = models.CharField(max_length=20)
    special_rules = MarkupField()

    class Meta:
        verbose_name_plural = 'Maps'
        verbose_name = 'Map'
        db_table = 'battlereport_map'
        app_label = 'battlereport'

class RosteredFight(models.Model):
    week = models.ForeignKey(BroadcastWeek)
    fight_type = models.ForeignKey(FightType)
    fought = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'battlereport_rosteredfight'
        app_label = 'battlereport'
