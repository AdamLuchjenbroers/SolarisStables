from genshi import Markup
from django.http import HttpResponse

from solaris.views import SolarisView

class ReferenceViewMixin(object):
    menu_selected = 'Reference'
    
    def get_context_data(self, **kwargs):
        try:
            page_context = super(ReferenceViewMixin, self).get_context_data(**kwargs)
        except AttributeError:
            page_context = Context()
        
        page_context['submenu'] = [
          {'title' : 'TechTree', 'url' : '/reference/techtree'},
          {'title' : 'Pilot Skills', 'url' : '/reference/pilotskills'},
          {'title' : 'Mechs', 'url' : '/reference/mechs'},       
        ]
        page_context['submenu_selected'] = self.__class__.submenu_selected
        return page_context


class ReferenceView(ReferenceViewMixin, SolarisView):
    
    def get(self, request, stable=None):
        body = Markup('<P>Reference Data Index to go here</P>')
        return HttpResponse(self.in_layout(body, request))
