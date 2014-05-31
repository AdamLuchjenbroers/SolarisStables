from django import template
from django.utils.safestring import mark_safe

register = template.Library()

class BasicFieldNode(template.Node):
    def __init__(self, field):
        self.field = template.Variable(field)
        self.template = template.loader.get_template('tags/form_basicfield.tmpl')
    
    def render(self, context):
        field_object = self.field.resolve(context)
        
        node_context = template.Context( {'field' : field_object }) 
        return mark_safe(self.template.render(node_context))
    

@register.tag(name="basic_field")
def do_basic_field(parser, token):
    try:
        (tag_name, field) = token.split_contents()
        
    except ValueError:
        raise template.TemplateSyntaxError("%r tag expects a single argument" % token.contents.split()[0])
    
    return BasicFieldNode(field)


