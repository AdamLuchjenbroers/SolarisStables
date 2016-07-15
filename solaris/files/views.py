#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View, FormView
from django.conf import settings

from solaris.utilities.loader import SSWLoader

from . import forms, models

import json
import uuid

class CreateTempMechView(FormView):
    form_class = forms.SSWUploadForm
    template_name = 'forms/upload_mech_form.html'

    def form_valid(self, form):
        return HttpResponse(json.dumps(form.instance.to_dict()))  
