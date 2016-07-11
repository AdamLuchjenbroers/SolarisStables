#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

from solaris.utilities.loader import SSWLoader

import .models

import uuid
import json


class CreateTempMechView(View):
    def post(self, request, **kwargs):

        ssw_upload_file = '%s' % uuid.uuid4()
        
        tempmech = models.TempMechFile.objects.create(filename=ssw_upload_file)
        
        ssw_upload_tmp = '%s%s' % (settings.SSW_UPLOAD_TEMP, ssw_upload_file)
        with open(ssw_upload_tmp, 'wb+') as tmp_output:
            for chunk in request.FILES['mech_ssw'].chunks():
                tmp_output.write(chunk)

        mech = SSWLoader(ssw_upload_file, basepath=settings.SSW_UPLOAD_TEMP)
        (mech_name, mech_code) = mech.get_model_details()
 
        result = {'mech_name' : mech_name, 'mech_code' : mech_code}
        return HttpResponse(json.dumps(result))
    
    
    def dispatch(self, request, *args, **kwargs):
        try: 
            return super(CreateTempMechView, self).dispatch(request, *args, **kwargs)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)