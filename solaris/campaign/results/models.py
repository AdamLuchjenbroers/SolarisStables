from django.db import models

from solaris.stablemanager.models import Stable
from solaris.stablemanager.mechs.models import Pilot, Mech

class StableEntry(models.Model):
    stable = models.ForeignKey(Stable)
    # Provided as an alternate, so stables that don't yet exist can still
    # have results entered.
    stable_name = models.CharField(max_length=50)
    credits_earned = models.IntegerField()
    training_points = models.IntegerField

    class Meta:
        verbose_name_plural = 'Stable Entries'
        verbose_name = 'Stable Entry'
        db_table = 'campaign_stableentry'
        app_label = 'campaign'
