from django.db import models

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()
    next = models.OneToOneField('Zodiac', related_name='prev', null=True)

    class Meta:
        verbose_name = 'Zodiac Sign'
        db_table = 'campaign_zodiac'
        app_label = 'campaign'
    
    def __unicode__(self):
        return self.sign

class BroadcastWeekManager(models.Manager):
    def current_week(self):
        return super(BroadcastWeekManager,self).get(next_week=None)

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    next_week = models.OneToOneField('BroadcastWeek', null=True, blank=True, related_name='prev_week')
    objects = BroadcastWeekManager()  
  
    def __unicode__(self):
        return 'Week %i' % self.week_number
        
    class Meta:
        verbose_name = 'Broadcast Week'
        db_table = 'campaign_broadcastweek'
        app_label = 'campaign'

    def advance(self):
        if self.next_week == None:            
            self.next_week = BroadcastWeek(
                week_number = self.week_number + 1
              , sign = self.sign.next
            )
            self.next_week.save()
            self.save()
        
        return self.next_week
    
