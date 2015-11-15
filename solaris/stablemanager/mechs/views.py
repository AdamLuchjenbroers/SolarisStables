from django.views.generic import TemplateView

from solaris.views import SolarisViewMixin
#from solaris.stablemanager.views import StableViewMixin, StableWeekMixin

from . import forms, models

class InitialMechPurchaseView(SolarisViewMixin, TemplateView):
    # Looks like Formset stuff isn't in Django main yet, so we'll have to improvise
    template_name = 'stablemanager/initial_mechs.tmpl'
    
    def get_context_data(self, **kwargs):
        context = super(InitialMechPurchaseView, self).get_context_data(**kwargs)
        
        context['mech_formset'] = forms.InitialMechsForm()
        context['submit'] = 'Purchase All'
        context['form_class'] = 'list initial-mechs'
        
        return context
    
