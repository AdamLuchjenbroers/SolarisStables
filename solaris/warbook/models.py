from django.db import models
from solaris.warbook.pilotskill.models import PilotTraitGroup

class House(models.Model):
    house = models.CharField(max_length=20, unique=True)
    blurb = models.TextField()
    house_disciplines = models.ManyToManyField(PilotTraitGroup, db_table='warbook_house_x_discipline')

    class Meta:
        verbose_name_plural = 'Houses'
        verbose_name = 'House'
        db_table = 'warbook_house'
        app_label = 'warbook'
    
    def __unicode__(self):
        return self.house
