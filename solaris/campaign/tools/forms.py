from django.forms import ChoiceField

from solaris.warbook.mech.forms import MechSearchForm
from solaris.warbook.models import house_list_as_opttree

roll_tables = (
  ('1D6', '1D6')
, ('D6-2', '2 D6 Tables')
, ('D6-3', '3 D6 Tables')
, ('1D20', '1D20')
)

class MechRollListForm(MechSearchForm):
    table_type = ChoiceField(label = 'Table Type', choices=roll_tables, required=True)
    available_to = ChoiceField(label='Faction', choices=house_list_as_opttree(), required=False)
