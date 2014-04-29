from django.db import models

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    prev_week = models.ForeignKey('BroadcastWeek', null=True, related_name='next_week')
    
    
