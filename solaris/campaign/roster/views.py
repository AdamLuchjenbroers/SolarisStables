from django.views.generic import TemplateView, View

from solaris.campaign.views import CampaignWeekMixin
from solaris.warbook.fightinfo.models import FightGroup

from . import forms

class FightRosterMixin(CampaignWeekMixin):
    def get_context_data(self, **kwargs):
        page_context = super(FightRosterMixin, self).get_context_data(**kwargs)

        group_list = []

        for group in FightGroup.objects.all():
            fights = self.week.fights.filter(fight_type__group=group)

            if fights.count() > 0:
              group_list.append({'name' : group.name, 'fights' : fights})

        page_context['group_list'] = group_list

        return page_context

class FightRosterView(FightRosterMixin, TemplateView):
    template_name = 'campaign/fights.html'
    view_url_name = 'campaign_fights'
    submenu_selected = 'Fights'

    def get_context_data(self, **kwargs):
        page_context = super(FightRosterView, self).get_context_data(**kwargs)

        page_context['add_form'] = forms.AddFightForm()

        return page_context
