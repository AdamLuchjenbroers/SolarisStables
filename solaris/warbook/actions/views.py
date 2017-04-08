
from django.views.generic import DetailView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

import json

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

class ActionDetailJsonView(DetailView):
    model = models.ActionType

    def get(self, request, *arg, **kwargs):
        action = self.get_object()

        action_data = {
          'group'         : action.group.group
        , 'action'        : action.action
        , 'description'   : action.description.rendered
        , 'base_cost'     : action.base_cost
        }

        return HttpResponse(json.dumps(action_data))
