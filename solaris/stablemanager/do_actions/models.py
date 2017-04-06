
from django.db import models

class StableAction(models.Model):
    week   = models.ForeignKey('StableWeek', related_name='actions', null=False)
    action = models.ForeignKey('warbook.ActionType', null=False)
    cost   = models.IntegerField(null=False)
    notes  = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Stable Actions'
        verbose_name = 'Stable Action'
        db_table = 'stablemanager_actions'
        app_label = 'stablemanager'
