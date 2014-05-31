from django.forms import ModelForm, Form, HiddenInput, IntegerField

from solaris.stablemanager.ledger.models import LedgerItem

class LedgerItemForm(ModelForm):
    id = IntegerField(widget=HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        super(LedgerItemForm, self).__init__(*args, **kwargs)
                
        self.fields['type'].widget = HiddenInput()
        
        self.fields['id'].initial = self.instance.pk
        if self.instance.pk:
            self.submit_action = 'Edit'
        else:
            self.submit_action = 'Add'
            
        self.postURL = '/stable/ledger'
        
        
    def set_tabs(self, form_tab):
        self.fields['description'].widget.attrs['tabindex'] = (form_tab * 3) - 2
        self.fields['cost'].widget.attrs['tabindex'] = (form_tab * 3) - 1
        self.submit_tab = form_tab * 3
        
    def set_postURL(self, postURL):
        self.postURL = postURL
                
    class Meta:
        model = LedgerItem
        
class LedgerDeleteForm(Form): 
    id = IntegerField(widget=HiddenInput, required=True)
    week = IntegerField(widget=HiddenInput, required=True)


    