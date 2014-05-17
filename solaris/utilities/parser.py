from math import floor

from django.utils.html import strip_tags

from solaris.warbook.equipment.models import Equipment

from solaris.utilities import translate


class SSWParseError(Exception):
    def __init__(self, mech, formerrors):
        self.value = 'Error parsing %s\n' % mech['ssw_filename']
        for (key, value) in formerrors.items():
            self.value += '\t%s: %s' % (key, strip_tags('%s' % value))
    def __str__(self):
        return repr(self.value)
   

class SSWMountedItem(dict):
    
    default_type = '?'   
    
    def __init__(self, eq_class=None):
        self['mech'] = None
            
        if eq_class == None:
            eq_class = self.__class__.default_type
                
        if self['ssw_name']:
            (self.equipment , created) = Equipment.objects.get_or_create(ssw_name=self['ssw_name'])
            
            self['equipment'] = self.equipment.id
            if created:
                self.equipment.name = self['name']
                self.equipment.equipment_class = eq_class
                self.equipment.save()
            
            if self.equipment.critical_func:
                self.criticals = self.equipment.criticals()
            else:
                self.criticals = None

    def mount(self, xmlnode, rear_firing=False, turret=False):
        #Most entries only record a single slot, and require that we 
        #extrapolate from there.
        self.extrapolated = False
        
        locations = xmlnode.xpath('./location|./splitlocation')
        
        self.mountings = {}
        for loc in locations:
            if loc.tag == 'location':
                index = [int(loc.get('index'))+1]
            if loc.tag == 'splitlocation':
                count = int(loc.get('number'))
                start = int(loc.get('index'))
                #TODO - Check if SSW counts forward or backward from the assigned index
                index = range(start+1, count+start+1)
            
            loc_code = loc.text.lower()
            
            if loc.text in self.mountings:
                self.mountings[loc_code].add_slot(index)
            else:
                self.mountings[loc_code] = SSWItemMounting(loc_code, index, rear=rear_firing, turret=turret)
            
        if len(self.mountings) == 0:
            self.mountings['--'] = SSWItemMounting('--', [])
    
    def extrapolate(self, criticals):
        if self.extrapolated:
            return
        
        if len(self.mountings) == 1: 
            loc = self.mountings.keys()[0]
            self.mountings[loc].extrapolate(criticals)
        self.extrapolated = True

class SSWLocation(dict):
    def __init__(self, mech, armour, code):
        self['mech'] = mech
        self['armour'] = armour

class SSWEquipment(SSWMountedItem):
    def __init__(self, xmlnode):
        (self['name'], rear, turret) = self.parse_name(xmlnode.xpath['./name[1]'].text)
        self.node_type = xmlnode.tag
        self['ssw_name'] = '%s - %s' % (self.node_type, self.name)
        
        self.mount(xmlnode, rear, turret)
        super(SSWEquipment,self).__init__()
        
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

    def __init__(self, xmlnode):
        self.mount(xmlnode, False, False)
        self.extrapolated = True
        
        structure_type = xmlnode.xpath('./type/text()')[0]
        self['ssw_name'] = 'Structure - %s' % structure_type
        self['name'] = structure_type
 
class SSWArmour(SSWMountedItem):
    
    default_type = 'S'
    
    def __init__(self, xmlnode):
         
        #Armour is stored as multiple single-slot assignments, so we can consider
        #it extrapolated already
        self.mount(xmlnode, False, False)
        self.extrapolated = True
        
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
        
class SSWEngine(SSWMountedItem):
    default_type = 'E'
    
    def __init__(self, xmlnode, gyro_criticals=4):
        self['ssw_name'] = 'Engine - %s' % xmlnode.text
        self['name'] = xmlnode.text
        
        self.mountings = {}
        
        if xmlnode.text == 'Compact Fusion Engine':
            self.mountings['ct'] = SSWItemMounting('ct', [1,2,3])
        else:
            self.mountings['ct'] = SSWItemMounting('ct', [1,2,3] + range(4 + gyro_criticals, 7 + gyro_criticals))
        
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
        
        super(SSWEngine, self).__init__()
        
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
    
class SSWMech(dict):
    def get_number(self, node, xpath):
        text = node.xpath(xpath)[0]
        return int(floor(float(text)))
    
    def __init__(self, xmlnode, ssw_filename, stock=True):
        self['tonnage'] = xmlnode.get('tons')
        self['mech_name'] = xmlnode.get('name')
        self['mech_code'] = xmlnode.get('model') or '--'
        
        self['is_omni'] = ( xmlnode.get('omnimech') == 'TRUE' )
                       
        self['credit_value'] = self.get_number(xmlnode, './cost/text()')
        
        if self['is_omni']:
            self['bv_value'] = 0
        else:
            self['bv_value'] = self.get_number(xmlnode, './battle_value/text()')
        
        self.equipment = []
        
        self.gyro = SSWGyro( xmlnode.xpath('./gyro')[0] )
        self.engine = SSWEngine( xmlnode.xpath('./engine')[0], gyro_criticals=self.gyro.criticals )
        self.armour = SSWArmour( xmlnode.xpath('./armor')[0] )
        self.structure = SSWStructure( xmlnode.xpath('./structure')[0] )
        
        self.equipment.append(self.gyro)
        self.equipment.append(self.engine)
        self.equipment.append(self.armour)        
        self.equipment.append(self.structure)        
        
        self['engine_rating'] = self.engine.rating
        self['stock_design'] = stock
        self['ssw_filename'] = ssw_filename
        
        self['tech_base'] = translate.tech_bases[ xmlnode.xpath('./techbase/text()')[0] ]
        self['motive_type'] = translate.motive_options[ xmlnode.xpath('./motive_type/text()')[0] ]
        
        self.type = xmlnode.xpath('./mech_type/text()')[0]
