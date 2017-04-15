from django.views.generic import TemplateView, View
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

import json

from solaris.views import SolarisViewMixin

from .models import Campaign, BroadcastWeek
from solaris.stablemanager.models import Stable

class CampaignViewMixin(SolarisViewMixin):
    week_navigation = False
    view_url_name = 'campaign_overview'
    can_advance_week = False

    def set_campaign(self):
        if not hasattr(self, 'campaign'):
            self.campaign = Campaign.objects.get_current_campaign()

    def dispatch(self, request, week=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

#        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
#            return HttpResponse('You do not have access to the campaign screen', 400)

        self.set_campaign()
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
        ]

        return page_context

class CampaignAdminMixin(CampaignViewMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to the campaign screen', 400)

        return super(CampaignAdminMixin, self).dispatch(request, *args, **kwargs)
  
class CampaignWeekMixin(CampaignViewMixin):
    week_navigation = True
    can_advance_week = True

    def dispatch(self, request, week=None, *args, **kwargs):
        self.set_campaign()

        if week == None:
            self.week = self.campaign.current_week()
        else:
            self.week = get_object_or_404(BroadcastWeek, week_number=week, campaign=self.campaign)

        return super(CampaignWeekMixin, self).dispatch(request, *args, **kwargs)

    def next_week_url(self):
        if self.week.next_week != None:
            return reverse(self.__class__.view_url_name, kwargs={'week' : self.week.next_week.week_number})
        else:
            return None

    def prev_week_url(self):
        if self.week.has_prev_week(): 
            return reverse(self.__class__.view_url_name, kwargs={'week' : self.week.prev_week.week_number})
        else:
            return None

    def get_context_data(self, **kwargs):
        page_context = super(CampaignWeekMixin, self).get_context_data(**kwargs)

        page_context['week'] = self.week
        page_context['prev_week_url'] = self.prev_week_url()
        page_context['next_week_url'] = self.next_week_url()

        week_args = { 'week' : self.week.week_number }
        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('campaign_overview', kwargs=week_args)}
        , {'title' : 'Actions', 'url' : reverse('campaign_actions', kwargs=week_args)}
        ]

        return page_context

class CampaignOverview(CampaignWeekMixin, TemplateView):
    template_name = 'campaign/overview.html'
    view_url_name = 'campaign_overview'
    submenu_selected = 'Overview'

    def get_context_data(self, **kwargs):
        page_context = super(CampaignOverview, self).get_context_data(**kwargs)

        active_stables = list(self.week.stableweek_set.all())
        active_stables.sort(key = lambda sw : -sw.prominence())

        page_context['active'] = active_stables
        page_context['inactive'] = Stable.objects.exclude(ledger__week=self.week)

        tech_counts = [sw.supply_contracts.count() for sw in active_stables]

        if len(tech_counts) > 0:
            page_context['min_techs'] = min(tech_counts)
            page_context['max_techs'] = max(tech_counts)
            page_context['avg_techs'] = sum(tech_counts) / len(tech_counts)
        else: 
            page_context['min_techs'] = "--"
            page_context['max_techs'] = "--"
            page_context['avg_techs'] = "--"

        return page_context

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
