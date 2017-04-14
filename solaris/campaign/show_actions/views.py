from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, Http404

import json

from solaris.stablemanager.models import Stable, StableWeek
from solaris.campaign.views import CampaignWeekMixin

class CampaignActionsView(CampaignWeekMixin, TemplateView):
    template_name = 'campaign/campaign_actions.html'
    view_url_name = 'campaign_actions'

    def get_context_data(self, **kwargs):
        page_context = super(CampaignActionsView, self).get_context_data(**kwargs)

        active_stables = list(self.week.stableweek_set.all())
        active_stables.sort(key = lambda sw : sw.week_started)

        page_context['active'] = active_stables
        page_context['inactive'] = Stable.objects.exclude(ledger__week=self.week)

        return page_context

class CampaignListStableActions(CampaignWeekMixin, DetailView):
    template_name = 'campaign/campaign_stableaction.html'
    view_url_name = 'campaign_actions'

    model = StableWeek

    def get_object(self, queryset=None):
        if queryset == None:
            queryset = self.get_queryset()

        try:
            stable_slug = self.kwargs.get('stable')
            week = self.kwargs.get('week',None)

            return StableWeek.objects.get(week=week, stable__stable_slug=stable_slug)
        except StableWeek.DoesNotExist:
            raise Http404('No record found')

class AjaxSetWeekStarted(CampaignWeekMixin, View):
    def post(self, request, week=None):
        postdata = request.POST.get('start_week', 'TRUE')
        started = ( postdata.upper() == 'TRUE' )

        if started:
            self.week.start_week()
        else:
            self.week.reset_week()

        return HttpResponse(json.dumps(True))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to start the week', status=400)

        return super(AjaxSetWeekStarted, self).dispatch(request, *args, **kwargs)
