from django.db import models
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict

import uuid

from solaris.utilities.loader import SSWLoader
from solaris.warbook.mech.models import MechDesign


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
    
    created = models.DateTimeField()

    def load_from_file(self, commit=True):
        if self.mech_name != None:
            # Already done.
            return
            
        (ssw_base, ssw_file) = self.ssw_file.path.rsplit('/',1)
        loader = SSWLoader(ssw_file, basepath=ssw_base)
        
        data = loader.get_model_details()
        
        self.mech_name   = data['mech_name']
        self.mech_code   = data['mech_code']
        self.is_omni     = data['is_omni']
        self.bv          = data['bv']
        self.cost        = int(data['cost'])
        self.tons        = data['tons']
        self.motive_type = data['motive_type']
        self.techbase    = data['techbase']
        
        try:
            if self.is_omni:
                self.design = MechDesign.objects.get(mech_name = self.mech_name, mech_code=self.mech_code, omni_loadout = 'Base')
            else:
                self.design = MechDesign.objects.get(mech_name = self.mech_name, mech_code=self.mech_code)
        except MechDesign.DoesNotExist:
            # Can't link it to an existing design
            pass
        
        if commit:
            self.save()
            
        if 'loadouts' in data:
            for (loadout, load_info) in data['loadouts'].items():
                new_loadout = self.loadouts.create(omni_loadout = loadout, bv=load_info['bv'], cost = load_info['cost'])                
                
                new_loadout.check_for_design()  
    
    def to_dict(self):
        result = model_to_dict(self, ('mech_name', 'mech_code', 'is_omni', 'bv', 'cost', 'tons', 'motive_type', 'techbase'))

        if self.design != None:
            result['design_status']= self.design.production_type
            result['design_status_text']= self.design.get_production_type_display()
        else:
            result['design_status'] = 'N'
            result['design_status_text'] = 'New Design'
        
        if self.is_omni:
            loadout_list = {}
            for loadout in self.loadouts.all():
                loadout_list[loadout.omni_loadout] = loadout.to_dict()
        
            result['loadouts'] = loadout_list
            
        return result
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            #self.load_from_file(commit=False)
            
        return super(TempMechFile, self).save(*args, **kwargs)
    
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
        result = model_to_dict(self, ('bv', 'cost'))
        
        if self.design != None:
            result['design_status']= self.design.production_type
            result['design_status_text']= self.design.get_production_type_display()
        else:
            result['design_status'] = 'N'
            result['design_status_text'] = 'New Design'
            
        return result
    
    def check_for_design(self):
        try:
            self.design = MechDesign.objects.get(
              mech_name = self.loadout_for.mech_name
            , mech_code = self.loadout_for.mech_code
            , omni_loadout = self.omni_loadout
            )
            self.save()
            
        except MechDesign.DoesNotExist:
            # Can't link it to an existing design
            pass        
    
    class Meta:
        verbose_name_plural = 'Temp Mech Configs'
        verbose_name = 'Temp Mech Config'
        db_table = 'temp_mechconfig'
        app_label = 'files'
