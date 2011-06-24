# -*- coding: iso-8859-1 -*-
from django.http import HttpResponse
from django_genshi import loader

def index(request):
    template = loader.get_template('basic.tmpl')
        
    output = template.generate(body="Hello World").render('html', doctype='html')
    return HttpResponse(output)
        
