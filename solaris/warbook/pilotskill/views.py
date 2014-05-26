from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView

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
