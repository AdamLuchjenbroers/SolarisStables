from django.db import models

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()
    next = models.OneToOneField('Zodiac', related_name='prev')
    
    def __unicode__(self):
        return self.sign

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    prev_week = models.OneToOneField('BroadcastWeek', null=True, related_name='next_week')
    
    def __unicode__(self):
        return 'Week %i' % self.week_number
    
    
