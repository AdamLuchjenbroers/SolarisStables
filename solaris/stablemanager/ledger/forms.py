from django.forms import ModelForm, HiddenInput

from solaris.forms import SolarisFixedFormMixin
from solaris.stablemanager.ledger.models import LedgerItem

class LedgerItemForm(SolarisFixedFormMixin, ModelForm):
    
    inner_form_template = 'stablemanager/ledger_item_add.tmpl'
    
    def __init__(self, *args, **kwargs):        
        self.fields['type'].widget = HiddenInput()
        
        super(LedgerItemForm, self).__init__(*args, **kwargs)
        
    def set_tabs(self, form_tab):
        self.fields['description'].widget.attrs['tabindex'] = (form_tab * 3) - 2
        self.fields['cost'].widget.attrs['tabindex'] = (form_tab * 3) - 1
        self.submit_tab = form_tab * 3
        
    def as_p(self):
        return self.template.generate(
             fields = self.getAllFields()
        ,    submit = 'Add'
        ,    post_url = '/stable/ledger'
        ,    submit_tab = self.submit_tab
        )
                
    class Meta:
        model = LedgerItem
    