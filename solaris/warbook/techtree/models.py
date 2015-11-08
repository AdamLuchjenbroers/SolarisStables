from django.db import models
from django.core.urlresolvers import reverse

from solaris.warbook.equipment.models import Equipment

class Technology(models.Model):
    
    categories = (            
                  ('weap' , 'Weaponry'),
                  ('equip', 'Equipment'),
                  ('cons' , 'Construction'),
                  ('ammo' , 'Ammunition'),
                  ('phys' , 'Physical Weapons'),
    )
    
    tiers = (
       
             ( 0 , 'Base Technology'),
             ( 1 , 'Star-League'),
             ( 2 , 'Advanced'),
             ( 3 , 'Experimental')
    )
  
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=8, choices=categories)
    urlname = models.CharField(max_length=20)
    description = models.TextField()
    base_difficulty = models.IntegerField()
    tier = models.IntegerField(choices=tiers)
    show = models.BooleanField(default=True)
    access_to = models.ManyToManyField(Equipment, db_table='warbook_tech_x_equipment')
 
    def __unicode__(self):
        if self.show:
            return self.name
        else:
            return '%s (Hidden)' % self.name
    
    def get_absolute_url(self):
        return reverse('technology', kwargs={'slug': self.urlname})
   
    class Meta:
        verbose_name_plural = 'Technologies'
        db_table = 'warbook_technology'
        app_label = 'warbook'


class TechnologyRollModifier(models.Model):
    technology = models.ForeignKey(Technology, related_name='modifiers')
    modifier   = models.IntegerField(default=2)
    condition  = models.CharField(max_length=120)
  
    class Meta:
        verbose_name_plural = 'Technology Roll Modifiers'
        db_table = 'warbook_technologyrollmodifier'
        app_label = 'warbook'
