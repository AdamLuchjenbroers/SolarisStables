from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from solaris.warbook import models
from solaris.cms.models import StaticContent
from solaris.core import render_page

def list_technologies(request, selected='>'):
    
    # Construct Technologies list
    tech_list = []       
    for (code, name) in models.Technology.categories:
        tech_list.append(
             ( name, [(tier, models.Technology.objects.filter(category=code, tier=tier, show=True)) for tier in range(1,4)] )
        )
    
    # Render Technologies List
    tmpl_tech = loader.get_template('tech_list.tmpl')    
    techtree = Markup(tmpl_tech.generate(techtree=tech_list))

    return render_page(body=techtree, selected=selected) 
  
def display_technology(request, technology='', selected=''):

    # Get Technology Information
    techdata = get_object_or_404(models.Technology, urlname=technology)
    modifiers = models.TechnologyRollModifier.objects.filter(technology=techdata)

    # Render Technology Detail
    tmpl_tech = loader.get_template('tech_detail.tmpl')
    description = Markup(techdata.description)
    
    body = Markup(tmpl_tech.generate(description=description, tech=techdata, modifiers=modifiers))
    return render_page(body=body, selected=selected) 