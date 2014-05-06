from django.conf.urls import patterns

from .ajax import JsonHouseDisciplines

urlpatterns = patterns('',
    (r'^house_disciplines/(?P<house_name>[^/]+)/?$', JsonHouseDisciplines.as_view() ), 
)