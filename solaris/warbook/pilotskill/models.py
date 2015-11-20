from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from decimal import Decimal

class TrainingCostManager(models.Manager):
    def upgrade_cost(self, training_type, from_skill, to_skill):
        return self.filter( training=training_type
                          , train_from__lte=from_skill
                          , train_to__gte=to_skill).aggregate(models.Sum('cost'))['cost__sum']

class TrainingCost(models.Model):
    training_options = (
        ('P', 'Piloting'),
        ('G', 'Gunnery'),
        ('S', 'Skills'),
    )
    training = models.CharField(max_length=1, choices=training_options)
    train_from = models.IntegerField()
    train_to = models.IntegerField()
    cost = models.IntegerField()

    objects = TrainingCostManager()

    class Meta:
        verbose_name_plural = 'Training Costs'
        verbose_name = 'Training Cost'
        db_table = 'warbook_trainingcost'
        app_label = 'warbook'
        unique_together = ('training','train_to')
        
    def __unicode__(self):
        return '%s %s' % (self.get_training_display(), self.train_to)
    

class PilotRank(models.Model):
    rank = models.CharField(max_length=20, unique=True)
    min_gunnery = models.IntegerField()
    min_piloting = models.IntegerField()
    skills_limit = models.IntegerField()
    auto_train_cp = models.IntegerField(default=0)
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
        return mark_safe(self.blurb)
  
    markup_blurb = property(get_markup_blurb, None)
  
    class Meta:
        verbose_name_plural = 'Pilot Trait Groups'
        verbose_name = 'Pilot Trait Group'
        db_table = 'warbook_pilottraitgroup'
        app_label = 'warbook'
    
    def get_absolute_url(self):
        return reverse('discipline', kwargs={'slug': self.urlname})
        
    def __unicode__(self):
        return '%s - %s' % (self.get_discipline_type_display(), self.name)
 
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
        db_table = 'warbook_pilottrait'
        app_label = 'warbook'
    
    def __unicode__(self):
        return self.name   


