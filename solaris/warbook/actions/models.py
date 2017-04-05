from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from markitup.fields import MarkupField

class ActionGroup(models.Model):
    group = models.CharField(max_length=50, blank=False, null=False)
    description = MarkupField()
    start_only = models.BooleanField(default=True)

    def __unicode__(self):
        return self.group

    class Meta:
        verbose_name_plural = 'Action Groups'
        verbose_name = 'Action Group'
        db_table = 'warbook_actiongroup'
        app_label = 'warbook'

class ActionType(models.Model):
    group = models.ForeignKey(ActionGroup, null=False, blank=False)
    action = models.CharField(max_length=50, blank=False, null=False)
    description = MarkupField()

    base_cost = models.IntegerField(default=1)
    base_cost_max = models.IntegerField(blank=True, null=True, default=None)

    max_per_week = models.IntegerField(default=1, blank=True, null=True)

    def __unicode__(self):
        if self.base_cost_max == None:
            return '%s (%i)' % (self.action, self.base_cost)
        else:
            return '%s (%i-%i)' % (self.action, self.base_cost, self.base_cost_max)

    class Meta:
        verbose_name_plural = 'Action Types'
        verbose_name = 'Action Type'
        db_table = 'warbook_actiontype'
        app_label = 'warbook'

