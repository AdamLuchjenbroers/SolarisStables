from django import forms

from solaris.stablemanager.models import Stable
from .widgets import StableImageInput

class StableLogoForm(forms.ModelForm):

    class Meta:
        model = Stable
        fields = ('stable_icon',)
        labels = { 
          'stable_icon' : 'Stable Logo:'
        } 
        widgets = {
          'stable_icon' : StableImageInput
        } 

class StableBannerForm(forms.ModelForm):

    class Meta:
        model = Stable
        fields = ('stable_bg',)
        labels = { 
          'stable_bg'   : 'Stable Banner:'
        } 
