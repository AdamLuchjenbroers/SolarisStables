from django.views.generic import TemplateView
from django.core.urlresolvers import reverse 

from solaris.views import SolarisViewMixin

class ReferenceViewMixin(SolarisViewMixin):
    menu_selected = 'Reference'
    
    def get_context_data(self, **kwargs):
        page_context = super(ReferenceViewMixin, self).get_context_data(**kwargs)
        
        page_context['submenu'] = [
          {'title' : 'TechTree', 'url' : reverse('tech_list')},
          {'title' : 'Pilot Skills', 'url' : reverse('pilot_skills')},
          {'title' : 'Pilot Issues', 'url' : reverse('pilot_issues')},
        ]
        
        if self.request.user.is_authenticated():
            page_context['submenu'] += [
                {'title' : 'Mechs', 'url' : reverse('mech_search')},       
            ]       
        
        page_context['submenu_selected'] = self.__class__.submenu_selected
               
        return page_context

class ReferenceView(ReferenceViewMixin, TemplateView):
    template_name = 'warbook/reference.tmpl'
