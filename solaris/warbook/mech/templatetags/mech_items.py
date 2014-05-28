from django.template import Context, loader
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="crit_table")
def crit_table(location):
   tmpl_table = loader.get_template('warbook/mech_crittable.tmpl')
   cnxt_table = Context({'object' : location})

   return mark_safe(
       tmpl_table.render(cnxt_table)
   )
