
from django.db import models

class StableActionManager(models.Manager):
    use_for_related_fields = True

    def start_of_week(self):
        return self.filter(action__group__start_only=True)

    def in_week(self):
        return self.filter(action__group__start_only=False)


class StableAction(models.Model):
    week   = models.ForeignKey('StableWeek', related_name='actions', null=False)
    action = models.ForeignKey('warbook.ActionType', null=False)
    cost   = models.IntegerField(null=False)
    notes  = models.CharField(max_length=256, null=True, blank=True)

    objects = StableActionManager()

    class Meta:
        verbose_name_plural = 'Stable Actions'
        verbose_name = 'Stable Action'
        db_table = 'stablemanager_actions'
        app_label = 'stablemanager'
