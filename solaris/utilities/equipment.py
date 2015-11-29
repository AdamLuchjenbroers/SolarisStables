from copy import deepcopy

#if 'equip_override' in globals():
#    print "Overriding Equipment Class"
#    Equipment = equip_override
#else:
from solaris.warbook.equipment.models import Equipment

class CriticalsList(object):
    def __init__(self, criticals=None):
        if criticals and isinstance(criticals, list):
            criticals.sort()
            self.slots = list(set(criticals)) #Deduplicate the list on assignment
        else:
            self.slots = []
            
    def __set__(self, value):
        if isinstance(value, list):
            value.sort()
            self.slots = value
        elif isinstance(value, str):
            self.slots = [int(s) for s in value.split(',')]
    
    def collapse(self):
        return ','.join(unicode(s) for s in self.slots)
        
    def __unicode__(self):
        return self.collapse()
            
    def __get__(self):
        return self.collapse()      
    
    def __str__(self):
        return self.collapse()
           
    def add(self, value, size=1):
        for new_slot in range(value, value+size):
            if not new_slot in self.slots:
                self.slots.append(new_slot)
                
        self.slots.sort()
    
    def last(self):
        return self.slots[-1]
    
    def __iadd__(self, other):
        try:
            for value in other:
                self.add(value)
        except TypeError:
            self.add(other)
        return self
    
    def __len__(self):
        return len(self.slots)
        
    def __add__(self, other):
        result = deepcopy(self)
        # Attempt to iterate over it, if that values assume it's a single value
        result += other
            
        return result
    
    def singleslot(self):
        """
        If the list contains only one slot, returns the value of that slot.
        Otherwise, return None
        """
        if len(self.slots) == 1:
            return self.slots[0]
        else:
            return None

class SSWItemMounting(dict):
    def __init__(self, location, slots, rear=False, turret=False):
        self.location_code = location
        self['location'] = None
        self['slots'] = CriticalsList(slots)
        self['rear_firing'] = rear
        self['turret_mounted'] = turret
        
    def add_slot(self, new_slots):
        self['slots'] += new_slots
        
    def size(self):
        return len(self['slots'])
    
    def last(self):
        return self['slots'].last()
        
    def extrapolate(self, count):
        start = self['slots'].singleslot()
        
        if start:
            self['slots'].add(start, int(count))
            
class SSWMountedItem(dict):
    
    default_type = '?'   
    default_extrapolated = False
    
    def __init__(self, eq_class=None):
        self['mech'] = None
        self.criticals = None
        self.mountings = {}
        self.extrapolated = self.__class__.default_extrapolated           
 
        if eq_class == None:
            eq_class = self.__class__.default_type
                
        if self['ssw_name']:
            (self.equipment , created) = Equipment.objects.get_or_create(ssw_name=self['ssw_name'])
            
            self['equipment'] = self.equipment.id
            if created:
                self.equipment.name = self['name']
                self.equipment.equipment_class = eq_class
                self.equipment.save()
            
    
    def total_mountings(self):
        return sum(self.mountings[k].size() for k in self.mountings.keys())         

    def mount(self, xmlnode, rear_firing=False, turret=False):
        #Most entries only record a single slot, and require that we 
        #extrapolate from there.
        self.extrapolated = self.__class__.default_extrapolated
        
        locations = xmlnode.xpath('./location|./splitlocation')        
        
        for loc in locations:
            if loc.tag == 'location':
                index = [int(loc.get('index'))+1]
            if loc.tag == 'splitlocation':
                count = int(loc.get('number'))
                start = int(loc.get('index'))
                index = range(start+1, count+start+1)
            
            loc_code = loc.text.lower()
            
            if loc_code in self.mountings:
                self.mountings[loc_code].add_slot(index)
            else:
                self.mountings[loc_code] = SSWItemMounting(loc_code, index, rear=rear_firing, turret=turret)
                
        if self.total_mountings() > 1:
            self.extrapolated = True
        elif self.total_mountings() == 0:
            self.mountings['--'] = SSWItemMounting('--', [])
            self.extrapolated = True #Has no slots
            
        if self.criticals and not self.extrapolated:
            self.extrapolate(self.criticals)
    
    def extrapolate(self, criticals):
        if self.extrapolated:
            return
        
        if len(self.mountings) == 1: 
            loc = self.mountings.keys()[0]
            self.mountings[loc].extrapolate(criticals)
            
        self.extrapolated = True
        
class SSWDerivedItem(SSWMountedItem):
    item_group = '?'
    
    def __init__(self, name, location, slot):
        self['name'] = name
        self['ssw_name'] = '%s - %s' % (self.__class__.item_group, name)
        
        super(SSWDerivedItem, self).__init__()        
        self.mountings[location] = SSWItemMounting(location, [slot])
        
        
class SSWActuator(SSWDerivedItem):
    default_extrapolated = True
    default_type = 'T'
    item_group = 'Actuator'
    
class SSWCockpitItem(SSWDerivedItem):
    default_extrapolated = True
    default_type = 'C'
    item_group = 'Cockpit'    
    
class SSWEnhancement(SSWMountedItem):
    default_type = 'Q'
    
    def __init__(self, xmlnode):
        enh_type = xmlnode.xpath('./type/text()')[0]
        self['name'] = enh_type
        self['ssw_name'] = 'Enhancement - %s' % enh_type

        super(SSWEnhancement, self).__init__()
        self.mount(xmlnode)       

class SSWEquipment(SSWMountedItem):
    
    default_type = '?'
    
    def __init__(self, xmlnode, fcs_artemisIV=False, fcs_artemisV=False, fcs_apollo=False):        
        (name, rear, turret) = self.parse_name(xmlnode.xpath('./name')[0].text)
        self['name'] = name
        
        try:
            self['name'].index('@')
            self['ssw_name'] = 'Ammo - %s' % name      
            super(SSWEquipment,self).__init__(eq_class='A')
        except ValueError:
            self['ssw_name'] = 'Equipment - %s' % name
            super(SSWEquipment,self).__init__()
        
        self.mount(xmlnode, rear, turret)        
        
    def parse_name(self, equipment_name):
        rear = False
        turret = False
        
        if equipment_name[0:3] == '(T)':
            turret = True
            equipment_name = equipment_name[4:]
            
        if equipment_name[0:3] == '(R)':
            rear = True
            equipment_name = equipment_name[4:]
            
        return (equipment_name, rear, turret)
        
class SSWStructure(SSWMountedItem):
    default_type = 'S'
    default_extrapolated = True

    def __init__(self, xmlnode):
        
        structure_type = xmlnode.xpath('./type/text()')[0]
        self['ssw_name'] = 'Structure - %s' % structure_type
        self['name'] = structure_type
        
        super(SSWStructure,self).__init__()        
        self.mount(xmlnode, False, False)
 
class SSWArmour(SSWMountedItem):
    
    default_type = 'S'
    
    def __init__(self, xmlnode):
        armorInfo = xmlnode.xpath('./*[not(self::type|self::location)]')
        self.armour = {}
        for location in armorInfo:
            self.armour[location.tag.lower()] = int(location.text)

        # Add an entry for the blank as well, just to make sure this gets populated correctly
        self.armour['--'] = 0
        
        armour_type = xmlnode.xpath('./type/text()')[0]
        self['ssw_name'] = 'Armour - %s' % armour_type
        self['name'] = armour_type
        
        super(SSWArmour,self).__init__()        
        self.mount(xmlnode, False, False)
        
class SSWEngine(SSWMountedItem):
    default_type = 'E'
    
    def __init__(self, xmlnode, gyro_criticals=4):
        self['ssw_name'] = 'Engine - %s' % xmlnode.text
        self['name'] = xmlnode.text
        
        super(SSWEngine, self).__init__()
               
        self.mountings['ct'] = SSWItemMounting('ct', [1,2,3])
        
        if xmlnode.text != 'Compact Fusion Engine':
            offset = 4 + (gyro_criticals or 4)            
            self.mountings['ct'].add_slot(range(offset, offset+3))
        
        side_count = 0
        if xmlnode.text == 'XL Engine':
            side_count = 3
        elif xmlnode.text == 'Light Fusion Engine':
            side_count = 2
        elif xmlnode.text == 'XXL Engine':
            side_count = 6
            
        if side_count > 0:
            right_start = int(xmlnode.get('rsstart')) + 1
            self.mountings['rt'] = SSWItemMounting('rt', range(right_start, right_start + side_count))
            
            left_start = int(xmlnode.get('lsstart')) + 1
            self.mountings['lt'] = SSWItemMounting('lt', range(left_start, left_start + side_count))
            
        self.rating = xmlnode.get('rating')    
        
class SSWGyro(SSWMountedItem):
    default_type = 'G'
    
    def __init__(self, xmlnode):
        self['ssw_name'] = 'Gyro - %s' % xmlnode.text
        self['name'] = xmlnode.text
        
        super(SSWGyro, self).__init__()
        
        self.mountings = {}
        if self.criticals:
            self.mountings['ct'] = SSWItemMounting('ct', range(4, 4+self.criticals))
            self.extrapolated = True
        else:
            self.mountings['ct'] = SSWItemMounting('ct', [4])
            self.extrapolated = False
    
    def extrapolate(self, criticals):
        self.criticals = criticals
        super(SSWGyro, self).extrapolate(criticals)
            
class SSWListItem(SSWMountedItem):
    
    def __init__(self, item_name, item_type, item_class, xml_location):
        self['name'] = item_name
        self['ssw_name'] = '%s - %s' % (item_type, item_name)
        
        super(SSWListItem, self).__init__(eq_class=item_class)
        
        code = xml_location.text.lower()
        index = int(xml_location.get('index')) + 1
        size = (self.criticals or 1)        
        
        self.mountings[code] = SSWItemMounting(code, range(index, index+size))
        

class SSWAttachedItem(SSWMountedItem):
    default_type = 'Q'
    default_extrapolated = False

    def __init__(self, item_name, attached_to, item_type='Equipment'):
        self['name'] = item_name
        self['ssw_name'] = '%s - %s' % (item_type, item_name)

        self.attached_to = attached_to
        self.loc = attached_to.mountings.keys()[0]
        
        super(SSWAttachedItem, self).__init__() 

    def extrapolate(self, criticals): 
        slots = [ self.attached_to.mountings[self.loc].last() + 1 + offset for offset in range(criticals) ]
        self.mountings[self.loc] = SSWItemMounting(self.loc, slots)
        self.extrapolated = True 
       
         
