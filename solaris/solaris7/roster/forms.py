from django import forms

from solaris.solaris7.fightinfo.models import fight_list_as_opttree
from solaris.warbook.mech.models import MechDesign

from . import models

class AddFightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.week = kwargs.pop('week', None)

        super(AddFightForm, self).__init__(*args, **kwargs)

        self.fields['fight_type'].choices = fight_list_as_opttree()

        omnis = MechDesign.objects.filter(is_omni=True, omni_basechassis=None).order_by('mech_name','mech_code')
        omni_choices = [(None, '---------'), ] +[ (m.id, '%s %s' % (m.mech_name, m.mech_code)) for m in omnis]
        self.fields['chassis'].choices = omni_choices

        self.fields['week'].initial = self.week

        self.fields['group_units'].required = False

    class Meta:
        model = models.RosteredFight
        fields = ('fight_type', 'fight_map', 'group_units', 'weightclass', 'group_tonnage', 'chassis', 'fight_class', 'purse', 'week')
        labels = {
          'fight_type' : 'Fight Type'
        , 'fight_map'  : 'Map'
        , 'chassis'    : 'Omnimech Chassis'
        , 'group_units' : 'Units'
        , 'group_tonnage' : 'Tonnage'
        , 'fight_class' : 'Fight Class (Manual Text)'
        }
        widgets = { 'week' : forms.HiddenInput }
