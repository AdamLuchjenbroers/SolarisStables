from django.db import models

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()
    next = models.OneToOneField('Zodiac', related_name='prev', null=True)
    
    def __unicode__(self):
        return self.sign

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    next_week = models.OneToOneField('BroadcastWeek', null=True, blank=True, related_name='prev_week')
    
    def __unicode__(self):
        return 'Week %i' % self.week_number
        
    def advance(self):
        if self.next_week == None:            
            self.next_week = objects.create(
                week_number = self.week_number + 1
              , sign = self.sign.next
            )
        
        return self.next_week
    
