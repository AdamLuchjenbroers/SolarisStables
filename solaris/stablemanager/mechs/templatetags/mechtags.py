from django import template

register = template.Library()

class MechStatusCSSNode(template.Node):
    def __init__(self, smw):
        self.smw_var = smw

    def render(self, context):
        smw = template.Variable(self.smw_var).resolve(context)

        if smw.mech_status == 'X':
            return 'mech-cored'
        elif smw.mech_status == 'R':
            return 'mech-removed'
        elif smw.mech_status == 'D':
            return 'mech-display'
        elif smw.mech_status == 'A':
            return 'mech-auction'
        else:
            return ''

@register.tag(name="mech_status_css")
def do_mech_status_css(parser, token):
    try:
        (tag_name, smw_var) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag expects one argument" % token.contents.split()[0])
    return MechStatusCSSNode(smw_var)    

