from genshi import Markup
from django.http import HttpResponse

from solaris.views import SolarisView

class ReferenceView(SolarisView):
    submenu = [
          {'title' : 'TechTree', 'url' : '/reference/techtree'},
          {'title' : 'Pilot Skills', 'url' : '/reference/pilotskills'},
          {'title' : 'Mechs', 'url' : '/reference/mechs'},       
        ]
    
    def get(self, request, stable=None):
        body = Markup('<P>Reference Data Index to go here</P>')
        return HttpResponse(self.in_layout(body, request))
