from django.conf.urls import patterns

from .ajax import JsonHouseDisciplines, JsonPriceOfMech, JsonBattleValueOfMech

urlpatterns = patterns('',
    (r'^house_disciplines/(?P<house_name>[^/]+)/?$', JsonHouseDisciplines.as_view() ), 
    (r'^mech/price-of/?$', JsonPriceOfMech.as_view() ),
    (r'^mech/bv-of/?$', JsonBattleValueOfMech.as_view() ),
)