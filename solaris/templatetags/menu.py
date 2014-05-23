from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="menu")
def menuitem(selected, args):
    (arg_name, arg_url) = args.split(',')
    if selected and arg_name.lower() == selected.lower():
        return mark_safe('<li class=\"selected\"><a href=\"%s\">%s</a></li>' % (arg_url, arg_name))
    else:
        return mark_safe('<li><a href=\"%s\">%s</a></li>' % (arg_url,arg_name))
 
