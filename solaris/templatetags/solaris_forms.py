from django import template
from django.utils.safestring import mark_safe

register = template.Library()

class TemplateFieldNode(template.Node):
    def __init__(self, field, template_name='tags/form_basicfield.tmpl', css_class='field'):
        self.field = template.Variable(field)
        self.template = template.loader.get_template(template_name)
        self.css_class = css_class
    
    def render(self, context):
        field_object = self.field.resolve(context)
        
        node_context = template.Context( {'field' : field_object, 'css_class' : self.css_class }) 
        return mark_safe(self.template.render(node_context))

@register.tag(name="basic_field")
def do_basic_field(parser, token):
    try:
        (tag_name, field) = token.split_contents()
        
    except ValueError:
        raise template.TemplateSyntaxError("%r tag expects a single argument" % token.contents.split()[0])
    
    return TemplateFieldNode(field)

@register.tag(name="column_field")
def do_column_field(parser, token):
    args = token.split_contents()
        
    if len(args) < 2:
        raise template.TemplateSyntaxError("%r tag expects a form field argument" % token.contents.split()[0])
    elif len(args) == 2:
        return TemplateFieldNode(args[1], template_name='tags/form_columnfield.tmpl', css_class='form_column')
    elif len(args) == 3:
        return TemplateFieldNode(args[1], template_name='tags/form_columnfield.tmpl', css_class=args[2])
    if len(args) > 3:
        raise template.TemplateSyntaxError("%r tag takes only a form field and optional CSS classname" % token.contents.split()[0])
        
    
    
