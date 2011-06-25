# -*- coding: iso-8859-1 -*-
from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from solaris.cms.models import StaticContent
from django.shortcuts import get_object_or_404


def static_content(request, selected='>'):
    navigation_options = [(page.title,page.url) for page in StaticContent.objects.filter(toplevel=True).order_by('order')]
    content = get_object_or_404(StaticContent, url='/%s' % selected).content
  
    template = loader.get_template('basic.tmpl')
    
    body = Markup(content)   
    output = template.generate(body=body, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)
        
