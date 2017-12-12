from django import forms

from solaris.warbook.fightinfo.models import fight_list_as_opttree
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


    def blank_to_none(self, fieldname):
        field = self.cleaned_data[fieldname]

        if field == '':
            return None
        else:
            return field

    def clean_chassis(self):
        return self.blank_to_none('chassis')

    def clean_group_units(self):
        return self.blank_to_none('group_units')

    def clean_group_tonnage(self):
        return self.blank_to_none('group_tonnage')

    def clean_weightclass(self):
        return self.blank_to_none('weightclass')
         
    def clean_week(self):
        return self.week

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
