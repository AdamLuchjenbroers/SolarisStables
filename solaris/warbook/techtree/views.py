#from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView

from solaris.views import SolarisViewMixin

from solaris.warbook.techtree import models
from solaris.warbook.views import ReferenceView

class TechnologyView(ReferenceView):
    submenu_selected = 'TechTree'

class TechnologyListView(SolarisViewMixin, TemplateView):
    menu_selected = 'Reference'
    submenu_selected = 'TechTree'
    template_name = 'warbook/techlist.tmpl'
    
    def get_context_data(self, **kwargs):
        page_context = super(TechnologyListView, self).get_context_data(**kwargs)
        tech_list = []
         
        for (code, name) in models.Technology.categories:
            print 'Adding %s (%s)' % (name, code)
            tech_list.append(
                { 'name' : name
                , 'tiers' : [{ 'number' : tier, 'techs' : models.Technology.objects.filter(category=code, tier=tier, show=True)} for tier in range(1,4)]}
            )
         
        page_context['techtree'] = tech_list
        
        return page_context

class TechnologyDetailView(TechnologyView):
    def get(self, request, technology='', **kwargs):
        # Get Technology Information
        techdata = get_object_or_404(models.Technology, urlname=technology)
        modifiers = models.TechnologyRollModifier.objects.filter(technology=techdata)

        # Render Technology Detail
        tmpl_tech = loader.get_template('warbook/techtree/tech_detail.genshi')
        description = Markup(techdata.description)
    
        body = Markup(tmpl_tech.generate(description=description, tech=techdata, modifiers=modifiers))
    
        return HttpResponse(self.in_layout(body, request))
