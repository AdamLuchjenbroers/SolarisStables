from django.db import models
from genshi import Markup
from decimal import Decimal

class PilotDiscipline(models.Model):
    name  = models.CharField(max_length=40)
    blurb = models.TextField()  
    urlname = models.CharField(max_length=20, unique=True)
  
    def get_markup_blurb(self):
        return Markup(self.blurb)
  
    markup_blurb = property(get_markup_blurb, None)
  
    class Meta:
        verbose_name_plural = 'Pilot Disciplines'
        verbose_name = 'Pilot Discipline'
        db_table = 'warbook_pilotdiscipline'
        app_label = 'warbook'
    
    def get_absolute_url(self):
        return '/reference/pilotskills/%s' % self.urlname
        
    def __unicode__(self):
        return self.name
    
 
class PilotTrait(models.Model):
    
    trait_list = (
                     ('T', 'Training')
                   , ('I', 'Issues') # Ego problems, family issues, etc
                   , ('O', 'Other') # Subdermal armour or other odd traits
                   )
    
    bv_modifiers = (
                    (Decimal('0.000'), 'No Modifier'    ),
                    (Decimal('0.050'), 'Piloting Skill' ),
                    (Decimal('0.200'), 'Gunnery Skill'  ),
                    )
    
    name  = models.CharField(max_length=40)
    description = models.TextField()
    discipline = models.ForeignKey(PilotDiscipline, null=True, blank=True, related_name='skills')
    bv_mod = models.DecimalField(max_digits=6 ,decimal_places=3 ,choices=bv_modifiers)
    trait_type = models.CharField(max_length=1, choices=trait_list, default='I')
    
    def bv_text(self):
        bv_description = self.get_bv_mod_display()
        return '%s (%0.2f)' % (bv_description, self.bv_mod)
      
    class Meta:
        verbose_name_plural = 'Pilot Traits'
        verbose_name = 'Pilot Trait'
        db_table = 'warbook_pilotability'
        app_label = 'warbook'
    
    def __unicode__(self):
        return self.name   
  
class PilotAbility(PilotTrait):
    
    class Meta:
        verbose_name_plural = 'Pilot Abilities'
        verbose_name = 'Pilot Ability'
        proxy = True

    def save(self, *args, **kwargs):
        self.trait_type = 'T'
        super(PilotAbility,self).save(*args, **kwargs)
