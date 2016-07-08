from django.contrib import admin
from django.db.models import Q
from django import forms

from solaris.warbook.pilotskill import models
    
class PilotTraitInline(admin.StackedInline):
    model = models.PilotTrait
    fields = (('name', 'table', 'item'), 'description', 'bv_mod')  

class PilotTraitGroupAdmin(admin.ModelAdmin):
    model = models.PilotTraitGroup
    inlines = [PilotTraitInline,]
    
class PilotRankForm(forms.ModelForm):
    class Meta:
        model = models.PilotRank
        fields = ('rank','min_gunnery','min_piloting', 'skills_limit', 'receive_tp', 'auto_train_cp',    'promotion','prominence_factor')
    
        labels = {
          'rank' : 'Rank Name'
        , 'min_gunnery' : 'Gunnery Limit'
        , 'min_piloting' : 'Piloting Limit'
        , 'skills_limit' : 'Skills Limit'
        , 'receive_tp' : 'Can Receive TP'
        , 'auto_train_cp' : 'Auto-Trained CP'
        , 'promotion' : 'Next Rank'
        , 'prominence_factor' : 'Prominence Multiplier'
        } 
    

class PilotRankAdmin(admin.ModelAdmin):
    model = models.PilotRank
    form = PilotRankForm
    fields = ('rank',('min_gunnery','min_piloting', 'skills_limit'), ('receive_tp', 'auto_train_cp'),('promotion','prominence_factor'))

