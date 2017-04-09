
from django.db import models

class StableActionManager(models.Manager):
    use_for_related_fields = True

    def start_of_week(self):
        return self.filter(action__group__start_only=True)

    def in_week(self):
        return self.filter(action__group__start_only=False)

    def spent_actions(self):
        count = self.aggregate(models.Sum('cost'))['cost__sum']

        if count == None:
            return 0
        else:
            return count

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

    def is_locked(self):
        return (self.action.group.start_only and self.week.week_started)
