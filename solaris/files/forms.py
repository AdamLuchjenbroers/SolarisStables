from django import forms 

from . import models

import uuid

class SSWUploadForm(forms.ModelForm):
    class Meta:
        model = models.TempMechFile
        fields = ('ssw_file',)
