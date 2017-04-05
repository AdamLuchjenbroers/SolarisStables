from django.contrib import admin
from django import forms

import solaris.warbook.techtree.models as tech_models
import solaris.warbook.techtree.admin as tech_admin

import solaris.warbook.pilotskill.models as pilot_models
import solaris.warbook.pilotskill.admin as pilot_admin

import solaris.warbook.equipment.models as equipment_models
import solaris.warbook.equipment.admin as equipment_admin

import solaris.warbook.actions.models as action_models
import solaris.warbook.actions.admin as action_admin

import solaris.warbook.models as base_models


class HouseForm(forms.ModelForm):
    house_disciplines = forms.ModelMultipleChoiceField(
                   queryset = pilot_models.PilotTraitGroup.objects.filter(discipline_type='T')
                 , label = 'House Training Disciplines'
                 , widget = admin.widgets.FilteredSelectMultiple('PilotTraitGroup', False)
                 , required = False
                 )
    class Meta:
        model = base_models.House
        fields = ('house','blurb','house_disciplines','selectable_disciplines','house_group','stable_valid') 

class HouseAdmin(admin.ModelAdmin):
    model = base_models.House
    form = HouseForm

    fields = ('house','blurb','house_disciplines','selectable_disciplines',('house_group','stable_valid')) 

# Import Houses
admin.site.register(base_models.House, HouseAdmin)

# Import Techtree
admin.site.register(tech_models.Technology, tech_admin.TechnologyAdmin)

# Import Pilot Skills and Disciplines
admin.site.register(pilot_models.PilotTraitGroup, pilot_admin.PilotTraitGroupAdmin)
admin.site.register(pilot_models.PilotRank, pilot_admin.PilotRankAdmin)
admin.site.register(pilot_models.TrainingCost)

# Import Equipment
admin.site.register(equipment_models.Equipment, equipment_admin.EquipmentAdmin )

# Import Actions
admin.site.register(action_models.ActionGroup, action_admin.ActionGroupAdmin)
admin.site.register(action_models.ActionType, action_admin.ActionTypeAdmin)
