#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View, FormView
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

from solaris.utilities.loader import SSWLoader

from . import forms, models

import json
import uuid

class CreateTempMechView(FormView):
    form_class = forms.SSWUploadForm
    template_name = 'forms/upload_mech_form.html'

    def form_valid(self, form):
        form.save()
        form.instance.load_from_file()
        
        result = form.instance.to_dict()
        
        return HttpResponse(json.dumps(result))  

    def form_invalid(self, form):
        result = {
          'success' : False
        , 'errors'  : { field : error for (field, error) in form.errors.items() }
        }

        return HttpResponse(json.dumps(result), 400)  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login('/', 'account_login', REDIRECT_FIELD_NAME)
        else:
            return super(CreateTempMechView, self).dispatch(request, *args, **kwargs)