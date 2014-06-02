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
        
class LocationValidationForm(ModelForm):    
    class Meta:
        model = MechDesignLocation
        
        
class MechEquipmentForm(ModelForm):
    class Meta:
        model = MechEquipment
        
class MountingForm(ModelForm):
    class Meta:
        model = Mounting
