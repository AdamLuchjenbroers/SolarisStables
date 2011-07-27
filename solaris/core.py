# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# Common functions that are useful in many places
# ------------------------------------------------------------
  
from django.http import HttpResponse
from django_genshi import loader
from solaris.cms.models import StaticContent
from django.http import HttpResponse

def render_page(body='', selected='', adminbar=False, request=None):
    # Get Navigation Menu / Templates 
    navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
    template = loader.get_template('layout.tmpl')
    
    output = template.generate(
      body=body
    , selected='/%s' % selected
    , menu=navigation_options
    , authenticated = request.user.is_authenticated()
    , username = request.user.username
    ).render('html', doctype='html')
    
    return HttpResponse(output)
  
