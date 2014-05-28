from django.views.generic import TemplateView, DetailView

from solaris.views import SolarisViewMixin

from solaris.warbook.techtree import models
from solaris.warbook.views import ReferenceViewMixin

class TechnologyListView(SolarisViewMixin, ReferenceViewMixin, TemplateView):
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

class TechnologyDetailView(SolarisViewMixin, ReferenceViewMixin, DetailView):
    submenu_selected = 'TechTree'
    template_name = 'warbook/techdetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.Technology
