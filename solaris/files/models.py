from django.db import models

class TempMechFile(models.Model):
    filename = models.CharField(max_length=50, unique=True)
    design = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    mech_name = models.CharField(max_length=50, null=True, blank=True)
    mech_code = models.CharField(max_length=50, null=True, blank=True)
    bv = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    tons = models.IntegerField(null=True, blank=True)
    
    def to_dict(self):
        return {}
    
    class Meta:
        verbose_name_plural = 'Temp Mechs'
        verbose_name = 'Temp Mech'
        db_table = 'temp_mechfile'
        app_label = 'files'
    

class TempMechLoadout(models.Model):
    loadout_for = models.ForeignKey(TempMechFile, related_name='loadouts')
    design = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    omni_loadout = models.CharField(max_length=30, null=True, blank=True)
    bv = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    
    def to_dict(self):
        return {}
    
    class Meta:
        verbose_name_plural = 'Temp Mech Configs'
        verbose_name = 'Temp Mech Config'
        db_table = 'temp_mechconfig'
        app_label = 'files'