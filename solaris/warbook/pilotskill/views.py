from django.views.generic import DetailView, ListView

from solaris.warbook.views import ReferenceViewMixin
from solaris.warbook.pilotskill import models

class DisciplineListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotDiscipline
    
class DisciplineDetailView(ReferenceViewMixin, DetailView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotDiscipline
