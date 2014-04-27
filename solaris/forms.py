
from django.forms import ModelForm

class SolarisModelForm(ModelForm):
    
    def as_p(self):
        # if self.errors
        # errorHeader =
        return ModelForm.as_p(self)