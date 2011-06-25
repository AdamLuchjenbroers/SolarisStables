from django.db import models
from math import ceil

class StaticContent(models.Model):
  title = models.CharField(max_length=20)
  url = models.CharField(max_length=20)
  content = models.TextField()
  toplevel = models.BooleanField()
  order = models.IntegerField()
  
  def __unicode__(self):
        return '%s (%s)' % (self.title, self.url)
