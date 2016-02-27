from django.forms import CharField, IntegerField, ChoiceField, Form

from solaris.warbook.models import House, house_list_as_opttree

class MechSearchForm(Form):
    mech_name = CharField(label='Mech Name', required=False)
    mech_code = CharField(label='Mech Code', required=False)
    tonnage_low = IntegerField(label='Min Tons', required=False)
    tonnage_high = IntegerField(label='Max Tons', required=False)
    cost_low = IntegerField(label='Min Cost', required=False)
    cost_high = IntegerField(label='Max Cost', required=False)
    bv_low = IntegerField(label='Min BV', required=False)
    bv_high = IntegerField(label='Max BV', required=False)
    
    available_opts = (('-', 'All Production Models'), ('me', 'My Stable')) \
                   + house_list_as_opttree()
    available_to = ChoiceField(label='Availability', choices=available_opts, required=False)
