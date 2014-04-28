from django.db import models

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKeyField(Zodiac)
    prev_week = models.ForeignKeyField(BroadcastWeek, null=True)
    next_week = models.ForeignKeyField(BroadcastWeek, null=True)
    
    
