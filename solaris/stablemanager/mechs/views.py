from django.views.generic import FormView, ListView

from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.ledger.models import LedgerItem

from . import forms, models

class InitialMechPurchaseView(StableViewMixin, FormView):
    # Looks like Formset stuff isn't in Django main yet, so we'll have to improvise
    template_name = 'stablemanager/initial_mechs.tmpl'
    form_class = forms.InitialMechsForm
    success_url = '/stable/initial-pilots'

    def form_valid(self, form):
        for mechform in form:
            models.StableMech.objects.create_mech( stable = self.stable
                                                 , purchased_as = mechform.design
                                                 , purchased_on = self.stable.get_stableweek()
                                                 , create_ledger = True
                                                 )
 
        return super(InitialMechPurchaseView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(InitialMechPurchaseView, self).get_context_data(**kwargs)
        
        context['submit'] = 'Purchase All'
        context['form_class'] = 'list initial-mechs'
        context['initial_balance'] = self.stable.get_stableweek().opening_balance
        
        return context

class StableMechsView(StableWeekMixin, ListView):
    submenu_selected = 'Mechs'
    template_name = 'stablemanager/stable_mechs.tmpl'
    model = models.StableMechWeek    

    def get_queryset(self):
        return self.stableweek.mechs.all()