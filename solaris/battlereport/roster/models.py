from django.db import models

from markitup.fields import MarkupField

from solaris.battlereport.models import BroadcastWeek

class FightGroup(models.Model):
    name = models.CharField(max_length=50)
    
class FightType(models.Model):
    group = models.ForeignKey(FightGroup)
    rules = MarkupField()

class Map(models.Model):
    name = models.CharField(max_length=20)
    special_rules = MarkupField()

class RosteredFight(models.Model):
    week = models.ForeignKey(BroadcastWeek)
    fight_type = models.ForeignKey(FightType)
    fought = models.BooleanField(default=False)
