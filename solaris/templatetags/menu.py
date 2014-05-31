from django import template
from django.utils.safestring import mark_safe

register = template.Library()

class MenuItemNode(template.Node):
    def __init__(self, title, url):
        self.title = title
        self.url = url
        
    def render(self, context):
        selected = template.Variable('selected').resolve(context)
        
        if selected and (selected.lower() == self.title.lower()):
            return mark_safe('<li class=\"selected\"><a href=\"%s\">%s</a></li>' % (self.url, self.title))
        else:
            return mark_safe('<li><a href=\"%s\">%s</a></li>' % (self.url, self.title))

@register.tag(name="menuitem")        
def do_menuitem(parser, token):    
    try:
        (tag_name, title, url) = token.split_contents()
        
    except ValueError:
        raise template.TemplateSyntaxError("%r tag expects two arguments argument" % token.contents.split()[0])
    
    return MenuItemNode(title, url)

@register.filter(name="menu")
def menuitem(selected, args):
    (arg_name, arg_url) = args.split(',')
    if selected and arg_name.lower() == selected.lower():
        return mark_safe('<li class=\"selected\"><a href=\"%s\">%s</a></li>' % (arg_url, arg_name))
    else:
        return mark_safe('<li><a href=\"%s\">%s</a></li>' % (arg_url,arg_name))
 

