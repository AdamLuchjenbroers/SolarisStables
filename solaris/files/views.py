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
import sys

class CreateTempMechView(FormView):
    form_class = forms.SSWUploadForm
    template_name = 'forms/upload_mech_form.html'
    form_url_name = 'files_upload_mech'

    def form_valid(self, form):
        form.save()
        
        try:
            form.instance.load_from_file()
        
            result = form.instance.to_dict()
      
            return HttpResponse(json.dumps(result))  
        except: 
            result = {
             'success' : False
            , 'errors'  : { '' : ['Failed to Parse Supplied File'] }
            }
            if settings.DEBUG:
                result['exception'] = sys.exc_info()
    
            form.instance.delete()
            return HttpResponse(json.dumps(result), status=400)  

    def form_invalid(self, form):
        result = {
          'success' : False
        , 'errors'  : { field : error for (field, error) in form.errors.items() }
        }

        return HttpResponse(json.dumps(result), status=400)  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login('/', 'account_login', REDIRECT_FIELD_NAME)
        else:
            return super(CreateTempMechView, self).dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(CreateTempMechView, self).get_context_data(**kwargs)
        
        context['form_url_name'] = self.__class__.form_url_name
        
        return context
