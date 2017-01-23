from django.views.generic import TemplateView, DetailView

from solaris.warbook.techtree import models
from solaris.warbook.views import ReferenceViewMixin

class TechnologyListView(ReferenceViewMixin, TemplateView):
    submenu_selected = 'TechTree'
    template_name = 'warbook/techlist.tmpl'
    
    def get_context_data(self, **kwargs):
        page_context = super(TechnologyListView, self).get_context_data(**kwargs)
        page_context['techtree'] = [{ 'number' : tier, 'techs' : models.Technology.objects.filter(tier=tier, show=True)} for tier in range(1,5)]
        
        return page_context

class TechnologyDetailView(ReferenceViewMixin, DetailView):
    submenu_selected = 'TechTree'
    template_name = 'warbook/techdetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.Technology
