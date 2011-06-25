# -*- coding: iso-8859-1 -*-
from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from solaris.urls import navigation_options

def static_content(request, selected='>', content=''):
    template = loader.get_template('basic.tmpl')
    
    body = Markup(content)   
    output = template.generate(body=body, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)
        
