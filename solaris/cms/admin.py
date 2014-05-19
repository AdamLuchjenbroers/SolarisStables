from django.contrib import admin
from solaris.cms import models

admin.site.register(models.NewsPost, NewsPostAdmin)

class NewsPostAdmin(admin.ModelAdmin)
    models = models.NewsPost
    
