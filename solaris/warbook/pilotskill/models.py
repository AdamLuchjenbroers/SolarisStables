from django.db import models
from genshi import Markup
  
  
class PilotDiscipline(models.Model):
  name  = models.CharField(max_length=40)
  blurb = models.TextField()  
  urlname = models.CharField(max_length=20)
  
  class Meta:
    verbose_name_plural = 'Pilot Disciplines'
    verbose_name = 'Pilot Discipline'
    db_table = 'warbook_pilotdiscipline'

  def __unicode__(self):
    return self.name
    
    
  
class PilotAbility(models.Model):
  bv_modifiers = (
    (0.00, 'No Modifier'    ),
    (0.05, 'Piloting Skill' ),
    (0.20, 'Gunnery Skill'  ),
  )
    
  name  = models.CharField(max_length=40)
  description = models.TextField()
  discipline = models.ForeignKey(PilotDiscipline)
  bv_mod = models.DecimalField(max_digits=6 ,decimal_places=3 ,choices=bv_modifiers)
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table = 'warbook_pilotability'
 