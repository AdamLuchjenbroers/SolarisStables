from markitup.fields import MarkupField

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

class WeightClass(models.Model):
    name = models.CharField(max_length=50)
    lower = models.IntegerField()
    upper = models.IntegerField()
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s (%i-%i tons)' % (self.name, self.lower, self.upper)

    class Meta:
        verbose_name_plural = 'Weight Classes'
        verbose_name = 'Weight Class'
        db_table = 'warbook_weightclass'
        app_label = 'warbook'
        ordering = ['lower',]

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
    group = models.ForeignKey('warbook.FightGroup', related_name='fights')
    name = models.CharField(max_length=50)
    urlname = models.CharField(max_length=50)
    blurb = models.CharField(max_length=255, blank=True)
    rules = MarkupField(blank=True)
    is_simulation = models.BooleanField(default=False)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.urlname == None:
            self.urlname = slugify(unicode(self.name))

        super(FightType, self).save()

    class Meta:
        verbose_name_plural = 'Fight Types'
        verbose_name = 'Fight Type'
        db_table = 'warbook_fighttype'
        app_label = 'warbook'
        ordering = ['order', 'name']
    
    def get_absolute_url(self):
        return reverse('fightinfo_detail', kwargs={'slug': self.urlname})
    
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

