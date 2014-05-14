from django.contrib import admin
from solaris.warbook.equipment import models
  
class EquipmentAdmin(admin.ModelAdmin):
    model = models.Equipment
