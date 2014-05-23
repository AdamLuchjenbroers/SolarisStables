from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="menu")
def menuitem(item):
    (url, title) = (item['url'], item['title'])
    return mark_safe('<li><a href \"%s\">%s</a></li>' % (url, title))
 
