from django import forms

from . import models
from solaris.warbook.actions.models import ActionGroup

class StableActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'stableweek' in kwargs:
            self.stableweek = kwargs['stableweek']
            del kwargs['stableweek']
        else:
            self.stableweek = None

        super(StableActionForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = self.get_choices()
        self.fields['action'].label = 'Actions:' 

    def get_choices(self):
        choices = (("","-- Select Action --"),)

        if self.stableweek != None and self.stableweek.week_started:
            available = ActionGroup.objects.exclude(start_only=True)
        else:
            available = ActionGroup.objects.all()

        for group in available:
            actionlist = tuple()

            for action in group.actions.all():
                if self.stableweek != None:
                    count_done = self.stableweek.actions.filter(action=action).count()
                else:
                    count_done = 0
                
                if count_done < action.max_per_week:
                    actionlist += ((action.id, str(action)),)
            
            if len(actionlist) > 0:   
                choices += ((group.group, actionlist),)
            
        return choices

    class Meta:
        model = models.StableAction
        fields = ('action', 'cost','notes')
