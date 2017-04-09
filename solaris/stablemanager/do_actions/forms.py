from django import forms

from . import models
from solaris.warbook.actions.models import ActionGroup

class StableActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'week_started' in kwargs:
            self.week_started = kwargs['week_started']
            del kwargs['week_started']
        else:
            self.week_started = False
 
        super(StableActionForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = self.get_choices()
        self.fields['action'].label = 'Actions:' 

    def get_choices(self):
        choices = (("","-- Select Action --"),)

        if self.week_started:
            available = ActionGroup.objects.exclude(start_only=True)
        else:
            available = ActionGroup.objects.all()

        for group in available:
            actionlist = tuple()

            for action in group.actions.all():
                actionlist += ((action.id, str(action)),)
               
            choices += ((group.group, actionlist),)
            
        return choices

    class Meta:
        model = models.StableAction
        fields = ('action', 'cost','notes')
