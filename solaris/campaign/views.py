from django.views.generic import TemplateView, View
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

import json

from solaris.views import SolarisViewMixin

from .models import Campaign, BroadcastWeek

class CampaignViewMixin(SolarisViewMixin):
    week_navigation = False
    view_url_name = 'campaign_overview'

    def set_campaign(self):
        if not hasattr(self, 'campaign'):
            self.campaign = Campaign.objects.get_current_campaign()

    def dispatch(self, request, week=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to the campaign screen', 400)

        self.set_campaign()
        return super(CampaignViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        page_context = super(CampaignViewMixin, self).get_context_data(**kwargs)

        page_context['campaign'] = self.campaign
        page_context['view_url_name'] = self.__class__.view_url_name
        page_context['week_navigation'] = self.__class__.week_navigation

        return page_context


class CampaignWeekMixin(CampaignViewMixin):
    week_navigation = True

    def dispatch(self, request, week=None, *args, **kwargs):
        self.set_campaign()

        if week == None:
            self.week = self.campaign.current_week()
        else:
            self.week = get_object_or_404(BroadcastWeek, week_number=week, campaign=self.campaign)

        return super(CampaignWeekMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        page_context = super(CampaignWeekMixin, self).get_context_data(**kwargs)

        page_context['week'] = self.week

        return page_context

class CampaignOverview(CampaignWeekMixin, TemplateView):
   template_name = 'campaign/overview.html'

class AjaxCreateCampaignView(CampaignViewMixin, View):
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
