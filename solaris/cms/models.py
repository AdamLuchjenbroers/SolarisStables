from django.db import models
from django.contrib.auth.models import User


from markitup.fields import MarkupField

class StaticContent(models.Model):
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=150)
    content = models.TextField()
    toplevel = models.BooleanField(default=False)
    order = models.IntegerField()
  
    def __unicode__(self):
        return '%s (%s)' % (self.title, self.url)
        
    class Meta:
        verbose_name = 'Static Content'
        verbose_name_plural = 'Static Content'
        app_label = 'cms'
    
   
class NewsPost(models.Model):
    title = models.CharField(max_length=120)
    poster = models.ForeignKey(User)
    content = MarkupField()
    post_date = models.DateField(auto_now_add=True)
  
    class Meta:
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'
        app_label = 'cms'
        permissions = (
                       ('post_news', 'Post News Items'),
                       )
        
  
    def __unicode__(self):
        return self.title

    def prepare(self):
        pass

