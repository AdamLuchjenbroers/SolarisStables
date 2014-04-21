from django.db import models
from genshi import Markup
from decimal import Decimal
  
class PilotDiscipline(models.Model):
    name  = models.CharField(max_length=40)
    blurb = models.TextField()  
    urlname = models.CharField(max_length=20)
  
    def get_markup_blurb(self):
        return Markup(self.blurb)
  
    markup_blurb = property(get_markup_blurb, None)
  
    class Meta:
        verbose_name_plural = 'Pilot Disciplines'
        verbose_name = 'Pilot Discipline'
        db_table = 'warbook_pilotdiscipline'
        app_label = 'warbook'
        
    def __unicode__(self):
        return self.name
    
    
  
class PilotAbility(models.Model):
    bv_modifiers = (
                    (Decimal('0.000'), 'No Modifier'    ),
                    (Decimal('0.050'), 'Piloting Skill' ),
                    (Decimal('0.200'), 'Gunnery Skill'  ),
                    )
    
    name  = models.CharField(max_length=40)
    description = models.TextField()
    discipline = models.ForeignKey(PilotDiscipline)
    bv_mod = models.DecimalField(max_digits=6 ,decimal_places=3 ,choices=bv_modifiers)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'warbook_pilotability'