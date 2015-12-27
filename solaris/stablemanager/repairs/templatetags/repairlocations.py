from django import template
from django.utils.safestring import mark_safe

register = template.Library()

class LocationDamageNode(template.Node):
   def __init__(self, location, template_path='stablemanager/tags/mech_repairlocation.html'):
        self.template = template.loader.get_template(template_path)

   def render(self, context):
        bill = template.Variable('bill').resolve(context)
        location = template.Variable('location').resolve(context)

        (structure, armour) = bill.getDamage(location.location.location)
        node_context = template.Context( {'location' : location, 'armour' : armour, 'structure' : structure })
        return mark_safe(self.template.render(node_context))

@register.tag(name='location_repair')
def do_location_repair(parser, token):
    try:
        (tag_name, location) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag expects a single argument" % token.contents.split()[0])
    return LocationDamageNode(location) 
