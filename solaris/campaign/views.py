from django.views.generic import TemplateView
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 
from django.shortcuts import redirect, get_object_or_404

from solaris.views import SolarisViewMixin

from .models import Campaign, BroadcastWeek

class CampaignWeekMixin(SolarisViewMixin):
    week_navigation = True

    def dispatch(self, request, week=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to the campaign screen', 400)

        self.campaign = Campaign.objects.get_current_campaign()

        if week == None:
            self.week = BroadcastWeek.objects.current_week()
        else:
            self.week = get_object_or_404(BroadcastWeek, week_number=week, campaign=self.campaign)

        return super(CampaignWeekMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        page_context = super(CampaignWeekMixin, self).get_context_data(**kwargs)

        page_context['campaign'] = self.campaign
        page_context['week'] = self.week
        page_context['week_navigation'] = self.__class__.week_navigation

        return page_context

class CampaignOverview(CampaignWeekMixin, TemplateView):
   template_name = 'campaign/overview.html'
