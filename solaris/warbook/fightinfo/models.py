from markitup.fields import MarkupField

from django.db import models

class FightGroup(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Fight Groups'
        verbose_name = 'Fight Group'
        db_table = 'warbook_fightgroup'
        app_label = 'warbook'
        ordering = ['order',]

class FightType(models.Model):
    group = models.ForeignKey('warbook.FightGroup')
    name = models.CharField(max_length=50)
    blurb = models.CharField(max_length=255, blank=True)
    rules = MarkupField(blank=True)
    is_simulation = models.BooleanField(default=False)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Fight Types'
        verbose_name = 'Fight Type'
        db_table = 'warbook_fighttype'
        app_label = 'warbook'
        ordering = ['order', 'name']
    
class Map(models.Model):
    name = models.CharField(max_length=20)
    special_rules = MarkupField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Maps'
        verbose_name = 'Map'
        db_table = 'warbook_map'
        app_label = 'warbook'
        ordering = ['name',]

class FightCondition(models.Model):
    name = models.CharField(max_length=20)
    rules = MarkupField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Fight Conditions'
        verbose_name = 'Fight Condition'
        db_table = 'warbook_fightconditions'
        app_label = 'warbook'
        ordering = ['name',]

