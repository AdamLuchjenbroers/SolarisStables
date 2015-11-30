from django.contrib import admin
from solaris.warbook.equipment import models
from solaris.warbook.techtree.models import Technology
  

class EquipmentTechnologyInline(admin.TabularInline):
    model = Technology.access_to.through
  
class EquipmentAdmin(admin.ModelAdmin):
    model = models.Equipment
    list_filter = ('equipment_class', 'record_status')
    inlines = [EquipmentTechnologyInline,]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ammo_for":
            kwargs["queryset"] = models.Equipment.objects.filter(has_ammo=True)
            
        return super(EquipmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
