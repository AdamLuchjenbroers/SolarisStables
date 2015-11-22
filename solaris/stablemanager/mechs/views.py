from django.views.generic import FormView

from solaris.stablemanager.views import StableViewMixin
from solaris.stablemanager.ledger.models import LedgerItem

from . import forms, models

class InitialMechPurchaseView(StableViewMixin, FormView):
    # Looks like Formset stuff isn't in Django main yet, so we'll have to improvise
    template_name = 'stablemanager/initial_mechs.tmpl'
    form_class = forms.InitialMechsForm
    success_url = '/stable/initial-pilots'

    def form_valid(self, form):
        for mechform in form:
            self.stablemech = models.StableMech.objects.create(stable=self.stable, purchased_as=mechform.design)
            self.stablemechweek = models.StableMechWeek.objects.create(
              stableweek = self.stable.get_stableweek()
            , stablemech = self.stablemech
            , current_design = mechform.design
            )

            self.ledgeritem = LedgerItem.objects.create (
              ledger = self.stable.get_stableweek()
            , description = 'Purchase - %s' % mechform.design.__unicode__()
            , cost = -mechform.design.credit_value
            , type = 'P'
            , tied = True
            , ref_mechdesign = mechform.design
            , ref_stablemech = self.stablemech
            , ref_stablemech_week = self.stablemechweek
            )
 
        return super(InitialMechPurchaseView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(InitialMechPurchaseView, self).get_context_data(**kwargs)
        
        context['submit'] = 'Purchase All'
        context['form_class'] = 'list initial-mechs'
        context['initial_balance'] = self.stable.get_stableweek().opening_balance
        
        return context
    
