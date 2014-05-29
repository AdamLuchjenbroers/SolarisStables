from django.http import HttpResponse
from django.template import Context
from django.views.generic import TemplateView 

from solaris.views import SolarisViewMixin

class ReferenceViewMixin(SolarisViewMixin):
    menu_selected = 'Reference'
    
    def get_context_data(self, **kwargs):
        page_context = super(ReferenceViewMixin, self).get_context_data(**kwargs)
        
        page_context['submenu'] = [
          {'title' : 'TechTree', 'url' : '/reference/techtree'},
          {'title' : 'Pilot Skills', 'url' : '/reference/pilotskills'},
          {'title' : 'Mechs', 'url' : '/reference/mechs'},       
        ]
        page_context['submenu_selected'] = self.__class__.submenu_selected
               
        return page_context

class ReferenceView(ReferenceViewMixin, TemplateView):
    template_name = 'warbook/reference.tmpl'
