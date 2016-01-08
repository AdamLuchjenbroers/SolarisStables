
from django.views.generic import TemplateView

from solaris.views import SolarisViewMixin

from .models import Campaign, BroadcastWeek

class CampaignWeekMixin(SolarisViewMixin):

    def get_context_data(self, **kwargs):
        page_context = super(CampaignWeekMixin, self).get_context_data(**kwargs)

        page_context['campaign'] = Campaign.objects.get_current_campaign()

        return page_context

class CampaignOverview(CampaignWeekMixin, TemplateView):
   template_name = 'campaign/overview.html'
