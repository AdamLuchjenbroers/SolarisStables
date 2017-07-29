from django.views.generic import DetailView, ListView

from solaris.warbook.views import ReferenceViewMixin

from . import models

class FightTypesView(ReferenceViewMixin, ListView):
    submenu_selected = 'Fight Types'
    template_name = 'warbook/fighttypes.html'
    model = models.FightGroup

class ConditionsView(ReferenceViewMixin, ListView):
    submenu_selected = 'Conditions'
    template_name = 'warbook/fightconditions.html'
    model = models.FightCondition

class MapsView(ReferenceViewMixin, ListView):
    submenu_selected = 'Maps'
    template_name = 'warbook/fightmaps.html'
    model = models.Map
