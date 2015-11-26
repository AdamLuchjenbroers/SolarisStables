from django.views.generic import TemplateView

from solaris.stablemanager.views import StableViewMixin
from solaris.stablemanager.ledger.models import LedgerItem

class CreateRepairBillView(StableViewMixin, TemplateView):
    template_name = 'stablemanager/stable_newrepair.html'

class RepairBillView(StableViewMixin, TemplateView):
    template_name = 'stablemanager/repair_bill.html'
