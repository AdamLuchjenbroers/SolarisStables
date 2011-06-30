from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from solaris.warbook import models
from solaris.cms.models import StaticContent

def list_technologies(request, selected='>'):
    navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
    template = loader.get_template('basic.tmpl')
    
    output = template.generate(body='Not Operational', selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)  
  
def display_technology(request, technology='', selected=''):
    navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
    techdata = get_object_or_404(models.Technology, urlname=technology)
  
    template = loader.get_template('basic.tmpl')
    
    body = Markup(techdata.description)   
    output = template.generate(body=body, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)