from django.db import models
from django.core.urlresolvers import reverse

from genshi import Markup
from decimal import Decimal

class PilotRank(models.Model):
    rank = models.CharField(max_length=20, unique=True)
    min_gunnery = models.IntegerField()
    min_piloting = models.IntegerField()
    skills_limit = models.IntegerField()
    promotion = models.ForeignKey('PilotRank', null=True, blank=True)    
        
    class Meta:
        verbose_name_plural = 'Pilot Ranks'
        verbose_name = 'Pilot Rank'
        db_table = 'warbook_pilotrank'
        app_label = 'warbook'
        
    def __unicode__(self):
        return self.rank

class PilotTraitGroup(models.Model):
    name  = models.CharField(max_length=40)
    blurb = models.TextField()  
    urlname = models.CharField(max_length=20, unique=True)
    
    discipline_options = (
                     ('T', 'Training')
                   , ('I', 'Issues') # Ego problems, family issues, etc
                   , ('O', 'Other') # Subdermal armour or other odd traits
                   )    
    discipline_type = models.CharField(max_length=1, choices=discipline_options, default='I')
  
    def get_markup_blurb(self):
        return Markup(self.blurb)
  
    markup_blurb = property(get_markup_blurb, None)
  
    class Meta:
        verbose_name_plural = 'Pilot Trait Groups'
        verbose_name = 'Pilot Trait Group'
        db_table = 'warbook_pilotdiscipline'
        app_label = 'warbook'
    
    def get_absolute_url(self):
        return reverse('discipline', kwargs={'slug': self.urlname})
        
    def __unicode__(self):
        return '%s - %s' % (self.get_discipline_type_display(), self.name)

class PilotDisciplineManager(models.Manager):
    def get_query_set(self):
        return super(PilotDisciplineManager,self).get_query_set().filter(discipline_type='T')

class PilotDiscipline(PilotTraitGroup):
    class Meta:
        verbose_name_plural = 'Pilot Disciplines'
        verbose_name = 'Pilot Discipline'
        app_label = 'warbook'
        proxy = True
        
    objects = PilotDisciplineManager()
    def __unicode__(self):
        return self.name
 
class PilotTrait(models.Model):
    bv_modifiers = (
                    (Decimal('0.000'), 'No Modifier'    ),
                    (Decimal('0.050'), 'Piloting Skill' ),
                    (Decimal('0.200'), 'Gunnery Skill'  ),
                    )
    
    name  = models.CharField(max_length=40)
    description = models.TextField()
    discipline = models.ForeignKey(PilotTraitGroup, null=True, blank=True, related_name='traits')
    bv_mod = models.DecimalField(max_digits=6 ,decimal_places=3 ,choices=bv_modifiers)
    
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

