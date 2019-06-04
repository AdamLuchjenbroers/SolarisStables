from django.db import models

from markitup.fields import MarkupField

from solaris.solaris7.models import BroadcastWeek

class RosteredFightCondition(models.Model):
    fight = models.ForeignKey('solaris7.RosteredFight')
    condition = models.ForeignKey('solaris7.FightCondition')
    annotation = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        if self.annotation not in (None, ''):
            return '%s (%s)' % (self.condition.name, self.annotation)
        else:
            return self.condition.name

    class Meta:
        db_table = 'solaris7_fight_x_condition'
        app_label = 'solaris7'

class RosteredFight(models.Model):
    week = models.ForeignKey('solaris7.BroadcastWeek', related_name='fights')
    fight_type = models.ForeignKey('solaris7.FightType')
    fight_map = models.ForeignKey('solaris7.Map')
    purse = models.IntegerField(blank=True, null=True)
    
    # For Omnimech fights and special challenges
    weightclass = models.ForeignKey('solaris7.WeightClass', null=True, blank=True)
    chassis = models.ForeignKey('warbook.MechDesign', null=True, blank=True)
    group_tonnage = models.IntegerField(null=True, blank=True)
    group_units = models.IntegerField(default=1)
    fight_class = models.CharField(max_length=40, blank=True) 

    fought = models.BooleanField(default=False)
    conditions = models.ManyToManyField('solaris7.FightCondition', through=RosteredFightCondition)

    def list_conditions(self):
        return 'TODO: List conditions'

    def __unicode__(self):
        return '%s %s : %s on %s' % (self.week, self.fight_type, self.fight_class, self.fight_map)

    def save(self, *args, **kwargs):
        if self.group_units == None:
           self.group_units = 1
 
        if self.weightclass != None:
            self.fight_class = str(self.weightclass)
            self.group_units = 1
            self.group_tonnage = self.weightclass.upper
        elif self.chassis != None:
            self.fight_class = str(self.chassis)
            self.group_units = 1
            self.group_tonnage = self.chassis.tonnage
        elif self.group_tonnage != None:
            if self.group_units > 1:
                self.fight_class = '%i units, %i tons' % (self.group_units, self.group_tonnage)
            else:
                self.fight_class = '%i tons' % self.group_tonnage
        else:
            # No modification, use fight class text that was provided manually.
            pass    

        super(RosteredFight, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Rostered Fights'
        verbose_name = 'Rostered Fight'
        db_table = 'solaris7_rosteredfight'
        app_label = 'solaris7'
        ordering = ['fight_type__order', 'group_units', 'weightclass__lower', 'group_tonnage']
