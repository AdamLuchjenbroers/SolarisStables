from django.contrib import admin
from solaris.model import cms, game

admin.site.register(game.Mech)
admin.site.register(game.Stable)
admin.site.register(cms.StaticContent)