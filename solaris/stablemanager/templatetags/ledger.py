from django.template import Context, loader, Library, Node, TemplateSyntaxError, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

register = Library()

class LedgerFormNode(Node):
    def __init__(self, form_variable, action='Add'):
        self.week = Variable('week.week_number')
        self.form = Variable(form_variable)
        
        self.template = loader.get_template('stablemanager/tags/stable_ledger_itemform.tmpl')
        self.node_context = Context( {'action' : action} )
        
        
    def render(self, context):
        week = Variable('week.week_number').resolve(context)
        
        if week:
            self.node_context['post_url'] = reverse('stable_ledger', kwargs={'week': week})
        else:
            self.node_context['post_url'] = reverse('stable_ledger_now')
            
        self.node_context['form'] = self.form.resolve(context)
        
        return mark_safe(self.template.render(self.node_context))       
    
class LedgerDeleteNode(Node):
    def __init__(self, form_variable):
        self.form = Variable(form_variable)
        
        self.template = loader.get_template('stablemanager/tags/stable_ledger_deleteitem.tmpl')
        self.node_context = Context( {'action' : 'X', 'post_url' : reverse('stable_ledger_delete')} )    
    def render(self, context):          
        self.node_context['form'] = self.form.resolve(context)
        
        return mark_safe(self.template.render(self.node_context))   

def do_ledger_form(parser, token, action='Add'):
    arguments = token.split_contents()
    
    if len(arguments) != 2:
        raise TemplateSyntaxError("%r tag expects a single  argument" % token.contents.split()[0])
    
    return LedgerFormNode(arguments[1], action=action)

@register.tag(name="ledger_add_form")
def do_ledger_add_form(parser, token):
    return do_ledger_form(parser, token, action='Add')

@register.tag(name="ledger_edit_form")
def do_ledger_edit_form(parser, token):
    return do_ledger_form(parser, token, action='Edit')

@register.tag(name="ledger_delete")
def do_ledger_delete(parser, token):
    arguments = token.split_contents()
    
    if len(arguments) != 2:
        raise TemplateSyntaxError("%r tag expects a single  argument" % token.contents.split()[0])
    
    return LedgerDeleteNode(arguments[1])
