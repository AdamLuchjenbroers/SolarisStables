from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from solaris.warbook import models
from solaris.cms.models import StaticContent

def list_technologies(request, selected='>'):
    navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
    
    tech_list = []   
    
    for (code, name) in models.Technology.categories:
        tech_list.append(
             ( name, [(tier, models.Technology.objects.filter(category=code, tier=tier)) for tier in range(0,4)] )
        )
                
    tmpl_page = loader.get_template('basic.tmpl')
    tmpl_tech = loader.get_template('tech_list.tmpl')
    
    techtree = Markup(tmpl_tech.generate(techtree=tech_list))
    output = tmpl_page.generate(body=techtree, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)  
  
def display_technology(request, technology='', selected=''):
    navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
    techdata = get_object_or_404(models.Technology, urlname=technology)
    modifiers = models.TechnologyRollModifier.objects.filter(technology=techdata)
  
    tmpl_page = loader.get_template('basic.tmpl')
    tmpl_tech = loader.get_template('tech_detail.tmpl')
    description = Markup(techdata.description)
    
    body = Markup(tmpl_tech.generate(description=description, tech=techdata, modifiers=modifiers))
    output = tmpl_page.generate(body=body, selected=selected, menu=navigation_options).render('html', doctype='html')
    return HttpResponse(output)