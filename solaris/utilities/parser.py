from math import floor

from django.utils.html import strip_tags


from solaris.utilities import translate
from solaris.utilities.equipment import SSWEquipment, SSWEngine, SSWGyro, SSWArmour, SSWStructure, SSWListItem, SSWActuator

class SSWParseError(Exception):
    def __init__(self, mech, formerrors):
        self.value = 'Error parsing %s\n' % mech['ssw_filename']
        for (key, value) in formerrors.items():
            self.value += '\t%s: %s' % (key, strip_tags('%s' % value))
    def __str__(self):
        return repr(self.value)

class SSWLocation(dict):
    def __init__(self, mech, armour, code):
        self['mech'] = mech
        self['armour'] = armour
        
class SSWQuadActuatorSet(list):
    def __init__(self):    
        for leg in ('frl', 'fll', 'rrl', 'rll'):
            self.append(SSWActuator('Hip', leg, 1))
            self.append(SSWActuator('Upper Leg', leg, 2))
            self.append(SSWActuator('Lower Leg', leg, 3))
            self.append(SSWActuator('Foot', leg, 4))
        

class SSWBipedActuatorSet(list):
    conditional_actuators = [
        ('lla', 'la', 'Lower Arm', 3),
        ('lh', 'la', 'Hand', 4),
        ('rla', 'ra', 'Lower Arm' ,3),
        ('rh', 'ra', 'Hand', 4),
    ]   
    
    def __init__(self, xmlnode):
        self.append(SSWActuator('Shoulder', 'la' ,1))
        self.append(SSWActuator('Upper Arm', 'la' ,2))
        self.append(SSWActuator('Shoulder', 'ra' ,1))
        self.append(SSWActuator('Upper Arm', 'ra' ,2))
        
        for (attr, location, name, slot) in SSWBipedActuatorSet.conditional_actuators:
            if xmlnode.get(attr) == 'TRUE':
                self.append(SSWActuator(name, location, slot))
            
        for leg in ('ll', 'rl'):
            self.append(SSWActuator('Hip', leg, 1))
            self.append(SSWActuator('Upper Leg', leg, 2))
            self.append(SSWActuator('Lower Leg', leg, 3))
            self.append(SSWActuator('Foot', leg, 4))
        

class SSWItemList(list):
    item_class = '?'
    item_group = '?'
    
    def __init__(self, xmlnode):
        item_name = xmlnode.xpath('./type/text()')[0]
        
        for location in xmlnode.xpath('./location'):
            self.append(SSWListItem(item_name, self.__class__.item_class, self.__class__.item_group, location))

class SSWHeatsinkList(SSWItemList):
    item_class = 'Heatsink'
    item_group = 'H'

class SSWJumpjetList(SSWItemList):
    item_class = 'Jumpjet'
    item_group = 'J'
    
class SSWBaseLoadout(list):
    pass   

class SSWLoadout(list):
    def __init__(self, xmlnode, motive_type='B'):       
        self += SSWHeatsinkList( xmlnode.xpath('./heatsinks')[0])
        
        if motive_type == 'B':
            self += SSWBipedActuatorSet( xmlnode.xpath('./actuators')[0] )
        else:
            self += SSWQuadActuatorSet()
        
        xml_jets = xmlnode.xpath('./jumpjets')
        
        for item in xmlnode.xpath('./equipment'):
            self.append(SSWEquipment(item))
        
        if xml_jets:
            self += SSWJumpjetList(xml_jets[0])
    
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
        
        self['tech_base'] = translate.tech_bases[ xmlnode.xpath('./techbase/text()')[0] ]
        self['motive_type'] = translate.motive_options[ xmlnode.xpath('./motive_type/text()')[0] ]
            
        self.gyro = SSWGyro( xmlnode.xpath('./gyro')[0] )
        self.engine = SSWEngine( xmlnode.xpath('./engine')[0], gyro_criticals=self.gyro.criticals )
        self.armour = SSWArmour( xmlnode.xpath('./armor')[0] )
        self.structure = SSWStructure( xmlnode.xpath('./structure')[0] )        
                
        self.equipment = SSWLoadout( xmlnode.xpath('./baseloadout')[0], motive_type=self['motive_type'])
        self.equipment.append(self.gyro)
        self.equipment.append(self.engine)
        self.equipment.append(self.armour)        
        self.equipment.append(self.structure) 
        
        
        
        self['engine_rating'] = self.engine.rating
        self['stock_design'] = stock
        self['ssw_filename'] = ssw_filename
        
        self.type = xmlnode.xpath('./mech_type/text()')[0]
