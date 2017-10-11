from django import forms

from solaris.warbook.fightinfo.models import fight_list_as_opttree

from . import models

class AddFightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddFightForm, self).__init__(*args, **kwargs)

        self.fields['fight_type'].label = 'Fight Type'
        self.fields['fight_type'].choices = fight_list_as_opttree()

    class Meta:
        model = models.RosteredFight
        fields = ('fight_type', 'fight_map', 'units', 'weightclass', 'tonnage', 'chassis', 'fight_class', 'purse')
