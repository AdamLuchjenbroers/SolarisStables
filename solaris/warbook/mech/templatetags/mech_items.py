from django.template import Context, Node, Variable, loader, Library, VariableDoesNotExist
from django.utils.safestring import mark_safe

register = Library()

class CrittableItemNode(Node):
    def __init__(self, template_name='warbook/tags/mech_crititem.html'):
        self.template = loader.get_template(template_name)
    
    def render(self, context):
        item = Variable('item').resolve(context)
        slot = Variable('forloop.counter').resolve(context)
        location = Variable('object.location_code').resolve(context)
        
        css_classes = 'mech-criticals-item'
        if item.is_crittable():
            css_classes += ' item-crittable'
        else:
            css_classes += ' item-noncrittable'
 
        if item.is_ammo():
            css_classes += ' item-ammo'
        try: 
            bill = Variable('bill').resolve(context)
            if bill.getCritical(location, slot):
                css_classes += ' item-critted'
        except VariableDoesNotExist:
            pass
        
        node_context = Context( {'item' : item, 'css_classes' : css_classes, 'location' : location, 'slot': slot }) 
        return mark_safe(self.template.render(node_context))

@register.tag(name="crit_item")
def do_crit_item(parser, token):
    return CrittableItemNode()
