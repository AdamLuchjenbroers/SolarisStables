from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse 

import json

from solaris.stablemanager.views import StableWeekMixin

from . import forms

class StableOptionsView(StableWeekMixin, TemplateView):
    submenu_selected = 'Options'
    template_name = 'stablemanager/stable_options.html'
    view_url_name = 'stable_options'

    def get_context_data(self, **kwargs):
        page_context = super(StableOptionsView, self).get_context_data(**kwargs)
        
        page_context['logo_form'] = forms.StableLogoForm(instance=self.stable)
        page_context['banner_form'] = forms.StableBannerForm(instance=self.stable)
        return page_context

class StableSetLogoView(StableWeekMixin, View):
    def post(self, request, week=None):
        form = forms.StableLogoForm(request.POST, request.FILES, instance=self.stable)

        if form.is_valid():
            form.save()
            return redirect(reverse('stable_options', kwargs={'week' : self.stableweek.week.week_number}))
        else:
            return HttpResponse('Failed', status=400)


