from django.contrib import admin
from solaris.warbook.equipment import models
  
class EquipmentAdmin(admin.ModelAdmin):
    model = models.Equipment
    list_filter = ('equipment_class', 'record_status')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ammo_for":
            kwargs["queryset"] = models.Equipment.objects.filter(has_ammo=True)
            
        return super(EquipmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)