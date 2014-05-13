from django.forms import ModelForm, HiddenInput, IntegerField

from solaris.forms import SolarisFixedFormMixin
from solaris.stablemanager.ledger.models import LedgerItem

class LedgerItemForm(SolarisFixedFormMixin, ModelForm):
    
    inner_form_template = 'stablemanager/ledger_item_add.tmpl'
    
    id = IntegerField(widget=HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        super(LedgerItemForm, self).__init__(*args, **kwargs)
                
        self.fields['type'].widget = HiddenInput()
        
        self.fields['id'].initial = self.instance.pk
        if self.instance.pk:
            self.submit_action = 'Edit'
        else:
            self.submit_action = 'Add'
        
        print self.fields
        
        
    def set_tabs(self, form_tab):
        self.fields['description'].widget.attrs['tabindex'] = (form_tab * 3) - 2
        self.fields['cost'].widget.attrs['tabindex'] = (form_tab * 3) - 1
        self.submit_tab = form_tab * 3
        
    def as_p(self):
        return self.template.generate(
             fields = self.getAllFields()
        ,    submit = self.submit_action
        ,    post_url = '/stable/ledger'
        ,    submit_tab = self.submit_tab
        )
                
    class Meta:
        model = LedgerItem
    