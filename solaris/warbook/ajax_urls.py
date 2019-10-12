from django.conf.urls import url

from .ajax import JsonHouseDisciplines, JsonPriceOfMech, JsonBattleValueOfMech

urlpatterns = [
    url(r'^house_disciplines/(?P<house_name>[^/]+)/?$', JsonHouseDisciplines.as_view() ), 
    url(r'^mech/price-of/?$', JsonPriceOfMech.as_view() ),
    url(r'^mech/bv-of/?$', JsonBattleValueOfMech.as_view() ),
]
