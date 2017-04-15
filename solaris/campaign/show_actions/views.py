from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse

import json

from solaris.stablemanager.models import Stable, StableWeek
from solaris.campaign.views import CampaignWeekMixin

class CampaignActionsView(CampaignWeekMixin, TemplateView):
    template_name = 'campaign/campaign_actions.html'
    view_url_name = 'campaign_actions'
    can_advance_week = False

    def get_context_data(self, **kwargs):
        page_context = super(CampaignActionsView, self).get_context_data(**kwargs)

        active_stables = list(self.week.stableweek_set.all())
        active_stables.sort(key = lambda sw : sw.week_started)

        page_context['active'] = active_stables
        page_context['inactive'] = Stable.objects.exclude(ledger__week=self.week)

        return page_context

class CampaignActionsListPart(CampaignActionsView):
    template_name = 'campaign/fragments/actions_list.html'

class CampaignListStableActions(CampaignWeekMixin, DetailView):
    template_name = 'campaign/campaign_stableaction.html'
    view_url_name = 'campaign_actions_stable'
    can_advance_week = False

    model = StableWeek

    def next_week_url(self):
        stableweek = self.get_object()

        if stableweek.next_week != None and stableweek.next_week.week_started:
            return reverse(self.__class__.view_url_name, kwargs={'week' : stableweek.next_week.week.week_number, 'stable' : self.kwargs.get('stable')})
        else:
            return None

    def prev_week_url(self):
        stableweek = self.get_object()

        if stableweek.has_prev_week() and stableweek.prev_week.week.week_started:
            return reverse(self.__class__.view_url_name, kwargs={'week' : stableweek.prev_week.week.week_number, 'stable' : self.kwargs.get('stable')})
        else:
            return None

    def get_object(self, queryset=None):
        if queryset == None:
            queryset = self.get_queryset()

        try:
            stable_slug = self.kwargs.get('stable')
            week = self.kwargs.get('week',None)

            return StableWeek.objects.get(week=week, stable__stable_slug=stable_slug)
        except StableWeek.DoesNotExist:
            raise Http404('No record found')

    def get_context_data(self, **kwargs):
        page_context = super(CampaignListStableActions, self).get_context_data(**kwargs)
 
        stableweek = page_context['object']

        page_context['ap_spent'] = stableweek.actions.spent_actions() 
        page_context['ap_avail'] = self.week.campaign.actions_per_week

        if stableweek.week_started:
            page_context['count_mechs']  = stableweek.mechs_count
            page_context['count_pilots'] = stableweek.pilot_count
            page_context['count_assets'] = stableweek.asset_count
        else:
            page_context['count_mechs'] = stableweek.mechs.count_nonsignature()
            page_context['count_pilots'] = stableweek.pilots.all_present().count()
            page_context['count_assets'] = page_context['count_mechs'] + page_context['count_pilots']

        return page_context 

    def get(self, request, *args, **kwargs):
        if not self.week.week_started:
            return HttpResponse('Cannot View Actions - Week Has Not Started', status=400)

        return super(CampaignListStableActions, self).get(request, *args, **kwargs)

class AjaxSetWeekStarted(CampaignWeekMixin, View):
    def post(self, request, week=None):
        postdata = request.POST.get('start_week', 'TRUE')
        started = ( postdata.upper() == 'TRUE' )

        if started:
            self.week.start_week()
        else:
            self.week.reset_week()

        data = {
          'week_started' : self.week.week_started
        , 'next_state'   : not self.week.week_started
        , 'button_text'  : 'Reset Week' if self.week.week_started else 'Start Week'
        }

        return HttpResponse(json.dumps(data))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to start the week', status=400)

        return super(AjaxSetWeekStarted, self).dispatch(request, *args, **kwargs)
