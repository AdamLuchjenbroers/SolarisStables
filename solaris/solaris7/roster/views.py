from django.views.generic import TemplateView, FormView, View
from django.http import HttpResponse 

from solaris.solaris7.views import Solaris7WeekMixin
from solaris.warbook.fightinfo.models import FightGroup

from . import forms

class FightRosterMixin(Solaris7WeekMixin):
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
    template_name = 'campaign/campaign_roster.html'
    view_url_name = 'campaign_fights'
    submenu_selected = 'Fights'

class FightRosterListPartView(FightRosterMixin, TemplateView):
    template_name = 'campaign/fragments/fights_list.html'
    view_url_name = 'campaign_fights'

class AddFightFormView(Solaris7WeekMixin, FormView):
    template_name = 'campaign/forms/add_rostered_fight.html'
    form_class = forms.AddFightForm
    success_url = '#'

    def get(self, request):
        form = forms.AddFightForm(week=self.week)
        return self.render_to_response(self.get_context_data(form=form)) 

    def post(self, request):
        form = forms.AddFightForm(data=request.POST, week=self.week)

        if form.is_valid():
            fight = form.save()
 
            return HttpResponse('Fight Added', status=201)
        else:
            return super(AddFightFormView, self).post(request)
