from django.forms import ModelForm, HiddenInput

from solaris.forms import SolarisFixedFormMixin
from solaris.stablemanager.ledger.models import LedgerItem

class LedgerItemForm(SolarisFixedFormMixin, ModelForm):
    
    inner_form_template = 'stablemanager/ledger_item_add.tmpl'
    
    def __init__(self, *args, **kwargs):
        SolarisFixedFormMixin.__init__(self, *args, **kwargs)
        ModelForm.__init__(self,*args, **kwargs)
        
        self.fields['type'].widget = HiddenInput()
        
    def as_p(self):
        return self.template.generate(
             fields = self.getAllFields()
        ,    submit = 'Add'
        ,    post_url = '/stable/ledger'
        )
                
    class Meta:
        model = LedgerItem
    