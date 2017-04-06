
from django.views.generic import DetailView, ListView

from solaris.warbook.views import ReferenceViewMixin
from . import models

class ActionGroupListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Actions'
    template_name = 'warbook/actiongroups.html'
    model = models.ActionGroup

class ActionGroupDetailView(ReferenceViewMixin, DetailView):
    submenu_selected = 'Actions'
    template_name = 'warbook/actiongroupdetail.html'
    slug_field = 'group__iexact'
    model = models.ActionGroup
