from django.views.generic import DetailView, ListView
from django.db.models import Q

from solaris.warbook.views import ReferenceViewMixin
from solaris.warbook.pilotskill import models

class DisciplineListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotTraitGroup
    queryset = models.PilotTraitGroup.objects.filter(discipline_type='T')
    
class DisciplineDetailView(ReferenceViewMixin, DetailView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotTraitGroup

class TraitsListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Pilot Issues'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotTraitGroup
    queryset = models.PilotTraitGroup.objects.filter(~Q(discipline_type='T'))

class TraitsDetailView(ReferenceViewMixin, DetailView):
    submenu_selected = 'Pilot Issues'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotTraitGroup