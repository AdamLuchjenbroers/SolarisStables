from django.db import models

from solaris.warbook.pilotskill.models import TrainingCost, PilotTrait
from solaris.stablemanager.mechs.models import PilotWeek

class TrainingEvent(models.Model):
    pilot = models.ForeignKey(PilotWeek)
    training = models.ForeignKey(TrainingCost)
    skill = models.ForeignKey(PilotTrait, null=True, blank=True)
    notes = models.CharField(max_length=50, null=True, blank=True)
