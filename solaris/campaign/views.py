from django.views.generic import ListView, View
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

import json

from solaris.views import SolarisViewMixin

from .models import Campaign
from solaris.solaris7.models import BroadcastWeek
from solaris.stablemanager.models import Stable

class CampaignListView(ListView):
    submenu_selected = 'Campaigns'
    template_name = 'campaign/campaign_list.html'
    model = Campaign

class CampaignViewMixin(SolarisViewMixin):
    week_navigation = False
    view_url_name = 'campaign_overview'
    can_advance_week = False

    def set_campaign(self, campaign_url):
        if not hasattr(self, 'campaign'):
            self.campaign = Campaign.objects.get(urlname = campaign_url)

    def dispatch(self, request, week=None, campaign_url=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

#        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
#            return HttpResponse('You do not have access to the campaign screen', 400)

        self.set_campaign(campaign_url)
        return super(CampaignViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        page_context = super(CampaignViewMixin, self).get_context_data(**kwargs)

        page_context['campaign'] = self.campaign
        page_context['view_url_name'] = self.__class__.view_url_name
        page_context['week_navigation'] = self.__class__.week_navigation
        page_context['view_can_advance'] = self.__class__.can_advance_week
        page_context['submenu_selected'] = self.__class__.submenu_selected

        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('campaign_overview_now') }
        , {'title' : 'Actions', 'url' : reverse('campaign_actions_now') }
        , {'title' : 'Tools', 'url' : reverse('campaign_tools_now') }
        ]

        return page_context

class CampaignAdminMixin(CampaignViewMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to the campaign screen', 400)

        return super(CampaignAdminMixin, self).dispatch(request, *args, **kwargs)

class AjaxCreateCampaignView(CampaignAdminMixin, View):
    def post(self, request):
        view = self.__class__.view_url_name
        if 'view' in request.POST:
            view = request.POST['view']

        try:
            week_no = int(request.POST['week'])
            week = self.campaign.weeks.get(week_number=week_no)

            nextweek = week.advance()
            nexturl = reverse(view, kwargs={'week' : nextweek.week_number})

            return HttpResponse(json.dumps(nexturl))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', 400)
        except BroadcastWeek.DoesNotExist:
            return HttpResponse('Source Broadcast Week not found', 404)
