# -*- coding: iso-8859-1 -*-
from django.http import HttpResponse
from django_genshi import loader
from solaris.urls import navigation_options

def render(request, selected='/', content='Hello World'):
    template = loader.get_template('basic.tmpl')
    
    #staticText = open(sourcefile)
    #body = Markup(staticText.read())
    
    output = template.generate(body=content, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)
        
