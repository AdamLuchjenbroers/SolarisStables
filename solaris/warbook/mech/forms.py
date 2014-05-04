'''
   ModelForm for validating Mech Data input loaded from SSW files
   This form is not intended to be rendered to a page
'''

from django.forms import ModelForm

from solaris.warbook.models import MechDesign

class MechValidationForm(ModelForm):

    class Meta:
        model = MechDesign
        
     
