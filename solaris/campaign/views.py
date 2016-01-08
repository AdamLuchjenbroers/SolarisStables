from django.views.generic import TemplateView
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse 

from solaris.views import SolarisViewMixin

from .models import Campaign, BroadcastWeek

class CampaignWeekMixin(SolarisViewMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), 'account_login', REDIRECT_FIELD_NAME)

        if not (request.user.has_perm('campaign.change_campaign') or request.user.is_superuser):
            return HttpResponse('You do not have access to the campaign screen', 400)

        return super(CampaignWeekMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        page_context = super(CampaignWeekMixin, self).get_context_data(**kwargs)

        page_context['campaign'] = Campaign.objects.get_current_campaign()

        return page_context

class CampaignOverview(CampaignWeekMixin, TemplateView):
   template_name = 'campaign/overview.html'
