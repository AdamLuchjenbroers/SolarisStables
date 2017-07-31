from django.contrib import admin

from . import models

class FightTypeInline(admin.StackedInline):
    model = models.FightType
    extra = 1

class FightGroupAdmin(admin.ModelAdmin):
    model = models.FightGroup
    inlines = [FightTypeInline,]
