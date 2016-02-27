from django.db import models
from solaris.warbook.pilotskill.models import PilotTraitGroup
from solaris.warbook.mech.models import MechDesign

house_group_options = (
    ('I', 'Inner Sphere')
,   ('M', 'Mercenaries')
,   ('P', 'Periphery')
,   ('C', 'Clan')
)

HouseGroups = dict(house_group_options)

class House(models.Model):
    house = models.CharField(max_length=50, unique=True)
    blurb = models.TextField()
    house_disciplines = models.ManyToManyField(PilotTraitGroup, blank=True, db_table='warbook_house_x_discipline')
    selectable_disciplines = models.IntegerField(default=2)
    produced_designs = models.ManyToManyField(MechDesign, blank=True, db_table='warbook_house_x_mechdesign')

    house_group = models.CharField(max_length=1, choices=house_group_options, default='I')
    stable_valid = models.BooleanField(default=True, verbose_name="Available for Stables")

    class Meta:
        verbose_name_plural = 'Houses'
        verbose_name = 'House'
        db_table = 'warbook_house'
        app_label = 'warbook'
    
    def __unicode__(self):
        return self.house
