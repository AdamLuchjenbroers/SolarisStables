from django.db import models

from markitup.fields import MarkupField

from solaris.campaign.models import BroadcastWeek

class RosteredFightCondition(models.Model):
    fight = models.ForeignKey('campaign.RosteredFight')
    condition = models.ForeignKey('warbook.FightCondition')
    annotation = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        if self.annotation not in (None, ''):
            return '%s (%s)' % (self.condition.name, self.annotation)
        else:
            return self.condition.name

    class Meta:
        db_table = 'campaign_fight_x_condition'
        app_label = 'campaign'

class RosteredFight(models.Model):
    week = models.ForeignKey('campaign.BroadcastWeek', related_name='fights')
    fight_type = models.ForeignKey('warbook.FightType')
    fight_map = models.ForeignKey('warbook.Map')
    purse = models.IntegerField(blank=True, null=True)
    
    # For Omnimech fights and special challenges
    weightclass = models.ForeignKey('warbook.WeightClass', null=True, blank=True)
    chassis = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    group_tonnage = models.IntegerField(null=True, blank=True)
    group_units = models.IntegerField(default=1)
    fight_class = models.CharField(max_length=40, blank=True) 

    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField('warbook.FightCondition', through=RosteredFightCondition)

    def weightclass_text(self):
        if self.units == 1:
            if self.chassis != None:
               return self.chassis
            elif self.weightclass != None:
               return self.weightclass
        
        if self.tonnage != None:
            return '%i Tons'
        else:
            return ''

    def save(self, *args, **kwargs):
        if self.group_units == None:
           self.group_units = 1
 
        if self.weightclass != None:
            self.fight_class = str(self.weightclass)
        elif self.tonnage != None:
            if self.tonnage_units > 1:
                self.fight_class = '%i units, %i tons' % (self.tonnage_units, self.tonnage)
            else:
                self.fight_class = '%i tons' % self.tonnage
        elif self.chassis != None:
            self.fight_class = str(self.chassis)
        else:
            # No modification, use fight class text that was provided manually.
            pass    

        super(RosteredFight, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'campaign_rosteredfight'
        app_label = 'campaign'
        ordering = ['fight_type__order', 'group_units', 'weightclass__lower', 'group_tonnage']
