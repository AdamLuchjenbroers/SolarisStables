from django.views.generic import TemplateView, View

from solaris.campaign.views import CampaignWeekMixin

class FightRosterView(CampaignWeekMixin, TemplateView):
    template_name = 'campaign/fights.html'
    view_url_name = 'campaign_fights'
    submenu_selected = 'Fights'

