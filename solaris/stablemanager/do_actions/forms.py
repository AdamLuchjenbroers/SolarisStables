from django import forms

from . import models
from solaris.warbook.actions.models import ActionGroup

class StableActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StableActionForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = self.get_choices()
        self.fields['action'].label = 'Actions:' 

    def get_choices(self):
        choices = (("","-- Select Action --"),)
        for group in ActionGroup.objects.all():
            actionlist = tuple()

            for action in group.actions.all():
                actionlist += ((action.id, str(action)),)
               
            choices += ((group.group, actionlist),)
            
        return choices

    class Meta:
        model = models.StableAction
        fields = ('week', 'action', 'cost','notes')
