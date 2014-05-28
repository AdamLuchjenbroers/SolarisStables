from django.views.generic import DetailView, ListView

from solaris.views import SolarisViewMixin

from solaris.warbook.views import ReferenceView, ReferenceViewMixin
from solaris.warbook.pilotskill import models

class DisciplineView(ReferenceView):
    submenu_selected = 'Pilot Skills'

class DisciplineListView(ReferenceViewMixin, SolarisViewMixin, ListView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotDiscipline
    
class DisciplineDetailView(ReferenceViewMixin, SolarisViewMixin, DetailView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotDiscipline
