from django.db import models
from django.core.urlresolvers import reverse
from math import ceil

from .refdata import locations_all, structure_entry, structure
from solaris.warbook.refdata import technology_tiers

class MechDesignManager(models.Manager):
    use_for_related_fields = True

    def production(self):
        return self.filter(production_type__in=('P','H'))

class MechDesign(models.Model):
    mech_name = models.CharField(max_length=50)
    mech_code = models.CharField(max_length=50)
    omni_loadout = models.CharField(max_length=30, default='Base', blank=True)
    stock_design = models.BooleanField(default=True)
    credit_value = models.IntegerField(null=True)
    bv_value = models.IntegerField(null=True)
    tonnage = models.IntegerField()
    engine_rating = models.IntegerField()
    is_omni = models.BooleanField(default=False)
    omni_basechassis = models.ForeignKey('MechDesign', null=True, blank=True, related_name="loadouts")

    ssw_filename = models.CharField(max_length=1024, blank=True, null=True)
    ssw_description = models.CharField(max_length=256, blank=True, null=True) 
    production_year = models.IntegerField(blank=True, null=True)

    required_techs = models.ManyToManyField('Technology', null=True, blank=True)
    
    motive_options = (
        ('B', 'Biped')
    ,   ('Q', 'Quad')
    )    
    motive_type = models.CharField(max_length=1, choices=motive_options)
    
    techbase_options = (
        ('I', 'Inner Sphere'),
        ('C', 'Clan'),
        ('M', 'Mixed')
    )  
    tech_base = models.CharField(max_length=1, choices=techbase_options)

    production_options = (
        ('P', 'Standard Production Design'),
        ('H', 'Historical Custom Design'),
        ('C', 'Customized Stable Design')
    )
    production_type = models.CharField(max_length=1, choices=production_options, default='P')    
    
    omni_basechassis = models.ForeignKey('MechDesign', null=True, blank=True, related_name='loadouts')
    tier = models.IntegerField(default=0, choices=technology_tiers)

    objects = MechDesignManager()

    def description(self):
        #Remove everything before the first , because Mech Name and Tonnage will be listed separately
        loc = self.ssw_description.find(', ') + 2
        return self.ssw_description[loc:]
    
    def omni_description(self):
        #Remove everything up to the armour amount, leaving only the loadout specific info.
        loc = self.ssw_description.find('Armor; ') + 7
        return self.ssw_description[loc:]        

    def total_armour(self):
        return (self.locations.aggregate( models.Sum('armour') ))['armour__sum']
    
    def reset_equipment(self):        
        for mount in self.loadout.all():
            mount.delete()

    def refresh_tier(self):
        self.tier = self.required_techs.aggregate(models.Max('tier'))['tier__max'] 
        self.save()
 
        return self.tier

    def get_production_loadouts(self):
        return self.get_loadouts(production_only=True)

    def get_loadouts(self, production_only=False):
        if self.is_omni:
            if self.omni_basechassis:
                loadouts = [self.omni_basechassis]
                omni_qset = self.omni_basechassis.loadouts
            else:
                loadouts = [self]
                omni_qset = self.loadouts

            if production_only:
                omni_loadouts = omni_qset.production()
            else:
                omni_loadouts = omni_qset.all()

            for omni_config in omni_loadouts:
                loadouts.append(omni_config)

            return loadouts
        else:
            return None
      
    def move_walk(self):
        return int(ceil(self.engine_rating / self.tonnage))
      
    def move_run(self):
        return int(ceil(self.move_walk() * 1.5))
       
    def move_jump(self):
        jump_mp = 0
        if not self.loadout:
            return 0
        
        for item in self.loadout.all():
            if item.equipment.equipment_class == 'J':
                jump_mp += 1
        return jump_mp
    
    def item_at(self, location, slot):
        mechLocation = self.locations.get(location__location=location)
        return mechLocation.item_at(slot)
        
    def directfire_tonnage(self):
        tons = 0
        for item in self.loadout.all():
            if item.is_directfire():
                tons += item.tonnage()
        return tons

    def all_equipment(self):
        from solaris.warbook.equipment.models import Equipment
        return Equipment.objects.filter(id__in=self.loadout.all().values('equipment'))   

    def get_engine_info(self):
        engine = self.loadout.filter(equipment__equipment_class='E').first()
        return (engine.equipment, self.engine_rating) 

    def get_gyro_info(self):
        gyro = self.loadout.filter(equipment__equipment_class='G').first()
        return (gyro.equipment, gyro.equipment.tonnage(self, units=1)) 

    def get_armour_info(self):
        armour = self.loadout.filter(equipment__equipment_class='S', equipment__ssw_name__istartswith='Armour').first() 
        return (armour.equipment, self.total_armour())

    def get_structure_info(self):
        structure = self.loadout.filter(equipment__equipment_class='S', equipment__ssw_name__istartswith='Structure').first() 
        return structure.equipment

    def equipment_manifest(self):
        manifest = {}
        for equip in self.all_equipment().exclude(equipment_class__in=('S','E','G')):
            manifest[equip] = self.loadout.filter(equipment=equip).count()

        return manifest
    
    def update_required_techs(self):
        from solaris.warbook.techtree.models import Technology
        self.required_techs.clear()

        for item in self.all_equipment():
            self.required_techs.add(*item.supplied_by.all())
            
        if self.is_omni:
            self.required_techs.add(Technology.objects.get(name='Omnimechs'))
            
        self.refresh_tier()

    def can_be_produced_with(self, equipment_list):
        # Check that all equipment on this mech can be found in the provided
        # list of available equipment
        return (self.all_equipment().exclude(pk__in=equipment_list).count() < 1)
    
    class Meta:
        unique_together = (('mech_name', 'mech_code', 'omni_loadout'), ('ssw_filename', 'omni_loadout'),)
        verbose_name_plural = 'Mech Designs'
        verbose_name = 'Mech Design'
        db_table = 'warbook_mechdesign'
        app_label = 'warbook'
        ordering = ['tonnage', 'mech_name', 'mech_code', 'omni_loadout']
        
    def __unicode__(self):
        if self.is_omni:
            return '%s %s (%s)' % (self.mech_name, self.mech_code, self.omni_loadout)
        else:
          return '%s %s' % (self.mech_name, self.mech_code)
    
    def all_locations(self):
        return { location.location_code() : location for location in self.locations.all() }  
    
    def get_absolute_url(self):
        if self.omni_loadout == 'Base':
            return reverse('mech_detail_base', kwargs={'name': self.mech_name, 'code': self.mech_code})
        else:
            return reverse('mech_detail', kwargs={'name': self.mech_name, 'code': self.mech_code, 'omni': self.omni_loadout})

class MechLocation(models.Model):
    location = models.CharField(max_length=3, unique=True, choices=locations_all)
    criticals = models.IntegerField()
    rear_of = models.ForeignKey('MechLocation', related_name='front_of', null=True)
    next_damage = models.ForeignKey('MechLocation', related_name='prev_damage', null=True)
    
    def structure(self, tonnage):
        table_entry = structure_entry(self.location)
        if table_entry != 'other':
            return structure[tonnage][table_entry]
        else:
            return None
    
    class Meta:
        verbose_name_plural = 'Mech Locations'
        verbose_name = 'Mech Location'
        db_table = 'warbook_mechlocation'
        app_label = 'warbook'
    
class MechDesignLocation(models.Model):
    mech = models.ForeignKey(MechDesign, related_name='locations')
    location = models.ForeignKey(MechLocation)
    armour = models.IntegerField()
    structure = models.IntegerField(null=True, blank=True)

    def is_front(self):
        return (self.location.rear_of == None)

    def item_at(self, slot):
        for item in self.criticals.all():
            if '%i' % slot in item.get_slots():
                return item.equipment
    
    def get_criticals(self):
        crit_table = [None] * self.location.criticals
        for item in self.criticals.all():
            for slot in item.get_slots():
                crit_table[int(slot)-1] = item
        return crit_table
    
    def location_code(self):
        return self.location.location
    
    def location_name(self):
        return self.location.get_location_display()

    def turret_tonnage(self):
        return sum( (item.equipment.equipment.tonnage() for item in self.criticals.filter(turret_mounted=True)))
        for item in self.criticals.filter(turret_mounted=True):
            tonnage
    
    class Meta:
        unique_together = (('mech','location'),)
        verbose_name_plural = 'Mech Design Locations'
        verbose_name = 'Mech Design Location'
        db_table = 'warbook_mechdesignlocation'
        app_label = 'warbook'
