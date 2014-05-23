from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="menu")
def menuitem(item):
    return mark_safe('<li><a href \"%s\">%s</a></li>' % (item['url'], item['title']))
 
