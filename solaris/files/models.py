from django.db import models
from django.conf import settings

import uuid

def uuid_tempfile(instance, filename):
    return '%s%s' % (settings.SSW_UPLOAD_TEMP, uuid.uuid4())

class TempMechFile(models.Model):
    ssw_file = models.FileField(upload_to=uuid_tempfile)
    design = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    mech_name = models.CharField(max_length=50, null=True, blank=True)
    mech_code = models.CharField(max_length=50, null=True, blank=True)
    is_omni = models.BooleanField(default=False)
    bv = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    tons = models.IntegerField(null=True, blank=True)
    motive_type = models.CharField(max_length=20, null=True, blank=True)
    techbase = models.CharField(max_length=20, null=True, blank=True)

    def load_from_file(self):
        if self.mech_name != None:
            # Already done.
            return

        loader = SSWLoader(self.ssw_file.path)  
    
    def to_dict(self):
        return { 'fixme' : 'Not Implemented Yet' }
    
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
