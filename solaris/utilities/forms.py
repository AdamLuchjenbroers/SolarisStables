'''
   ModelForm for validating Mech Data input loaded from SSW files
   This form is not intended to be rendered to a page
'''

from django.forms import ModelForm
from solaris.warbook.mech.models import MechDesign, MechDesignLocation
from solaris.warbook.equipment.models import Mounting, MechEquipment

class MechValidationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MechValidationForm,self).__init__(*args, **kwargs)
        
    class Meta:
        model = MechDesign
        fields = ( 'mech_name', 'mech_code', 'omni_loadout', 'stock_design', 'credit_value', 'bv_value', 'tonnage'
                 , 'engine_rating', 'is_omni', 'omni_basechassis', 'ssw_filename', 'motive_type', 'tech_base'
                 , 'production_type', 'omni_basechassis') 
        
class LocationValidationForm(ModelForm):    
    class Meta:
        model = MechDesignLocation
        fields = ('mech', 'location', 'armour', 'structure') 
        
class MechEquipmentForm(ModelForm):
    class Meta:
        model = MechEquipment
        fields = ('mech', 'equipment')
 
class MountingForm(ModelForm):
    class Meta:
        model = Mounting
        fields = ('location', 'equipment', 'slots', 'rear_firing', 'turret_mounted')
