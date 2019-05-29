from django.views.generic import TemplateView
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from solaris.campaign.views import CampaignViewMixin

from .models import BroadcastWeek, SolarisCampaign

class Solaris7ViewMixin(CampaignViewMixin):

    def set_campaign(self, campaign_url):
        super(Solaris7ViewMixin, self).set_campaign(campaign_url)

        # Fetch the campaign-type specific object as well.
        self.solaris_campaign = get_object_or_404(SolarisCampaign, campaign=self.campaign)

class Solaris7WeekMixin(Solaris7ViewMixin):
    week_navigation = True
    can_advance_week = True

    def dispatch(self, request, *args, **kwargs):
        self.set_campaign(kwargs.get('campaign_url'))

        week = kwargs.pop('week', None)
        if week == None:
            #self.week = self.campaign.current_week()
            #FIXME: Work-around
            self.week = get_object_or_404(BroadcastWeek, next_week=None, campaign=self.solaris_campaign)
        else:
            self.week = get_object_or_404(BroadcastWeek, week_number=week, campaign=self.solaris_campaign)

        return super(Solaris7WeekMixin, self).dispatch(request, *args, **kwargs)

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
        page_context = super(Solaris7WeekMixin, self).get_context_data(**kwargs)

        page_context['week'] = self.week
        page_context['prev_week_url'] = self.prev_week_url()
        page_context['next_week_url'] = self.next_week_url()

        week_args = { 'week' : self.week.week_number, 'campaign_url' : self.campaign.urlname }
        page_context['submenu'] = [
          {'title' : 'Overview', 'url' : reverse('campaign_overview', kwargs=week_args)}
        , {'title' : 'Actions', 'url' : reverse('campaign_actions', kwargs=week_args)}
#        , {'title' : 'Fights', 'url' : reverse('campaign_fights', kwargs=week_args)}
        , {'title' : 'Tools', 'url' : reverse('campaign_tools', kwargs=week_args)}
        ]

        return page_context

class Solaris7Overview(Solaris7WeekMixin, TemplateView):
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
