from django.contrib import admin
from solaris.cms import models

class NewsPostAdmin(admin.ModelAdmin):
    models = models.NewsPost
    
admin.site.register(models.NewsPost, NewsPostAdmin)
