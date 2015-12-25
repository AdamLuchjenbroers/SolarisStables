from math import floor

from django.utils.html import strip_tags


from solaris.utilities import translate
from solaris.utilities.equipment import SSWTurret, SSWEquipment, SSWEnhancement, SSWEngine, SSWGyro, SSWArmour, SSWStructure, SSWListItem, SSWMultiSlot, SSWActuator, SSWCockpitItem, SSWAttachedItem

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
        
class SSWCockpitSet(list):
    def __init__(self, xmlnode):
        cockpit_layout = xmlnode.xpath('./type/text()')[0]
        
        if cockpit_layout == 'Torso-Mounted Cockpit':
            self.torso_cockpit(xmlnode, cockpit_layout)
        elif cockpit_layout in ('Standard Cockpit', 'Primitive Cockpit', 'Industrial Cockpit', 'Industrial w/ Adv. FC', 'Primitive Industrial Cockpit'):
            self.normal_cockpit(xmlnode, cockpit_layout)
        elif cockpit_layout == 'Small Cockpit':
            self.small_cockpit(xmlnode, cockpit_layout)
        else:
            print 'Unrecognised Cockpit Layout: %s' % cockpit_layout
    
    def normal_cockpit(self, xmlnode, name):
        self.append(SSWCockpitItem('Life Support', 'hd', 1))
        self.append(SSWCockpitItem('Sensors', 'hd', 2))
        self.append(SSWCockpitItem(name, 'hd', 3))
        self.append(SSWCockpitItem('Sensors', 'hd', 5))
        self.append(SSWCockpitItem('Life Support', 'hd', 6))
        
    def small_cockpit(self, xmlnode, name):
        self.append(SSWCockpitItem('Life Support', 'hd', 1))
        self.append(SSWCockpitItem('Sensors', 'hd', 2))
        self.append(SSWCockpitItem(name, 'hd', 3))
        self.append(SSWCockpitItem('Sensors', 'hd', 4))       
        
    def torso_cockpit(self, xmlnode, cockpit):
        
        def parse_location(location, name):
            slot = int(location.get('index'))+1
            loc_code = location.text.lower()
            self.append(SSWCockpitItem(name, loc_code, slot))        
        #Torso mounted cockpits store the locations in a particular order
        #and provide no other information to identify them
        location_set = xmlnode.xpath('location')
        
        parse_location(location_set[0], cockpit)
        parse_location(location_set[1], 'Sensors')
        parse_location(location_set[2], 'Life Support')
        parse_location(location_set[3], 'Life Support')
        
        # 2 Sensor packages are also included in the head (Tactical Operations, pg.300)
        self.append(SSWCockpitItem('Sensors', 'hd', 1))
        self.append(SSWCockpitItem('Sensors', 'hd', 2))
        
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
        self.parse_items(xmlnode, item_name)
       
    def parse_items(self, xmlnode, item_name):
        for location in xmlnode.xpath('./location'):
            self.append(SSWListItem(item_name, self.__class__.item_class, self.__class__.item_group, location))

class SSWHeatsinkList(SSWItemList):
    item_class = 'Heatsink'
    item_group = 'H'

class SSWJumpjetList(SSWItemList):
    item_class = 'Jumpjet'
    item_group = 'J'
    
class SSWLegAESList(SSWItemList):
    item_class = 'AES'
    item_group = 'Q'

    def __init__(self, xmlnode):
        self.parse_items('Leg AES', item_name)
    

class SSWLoadout(list):
    def __init__(self, xmlnode, motive_type='B'):
        xml_heatsinks = xmlnode.xpath('./heatsinks')
        if xml_heatsinks:       
            self += SSWHeatsinkList(xml_heatsinks[0])
        
        self.fcs_artemis_iv = (xmlnode.get('fcsa4') == 'TRUE')
        self.fcs_artemis_v = (xmlnode.get('fcsa5') == 'TRUE')
        self.fcs_apollo = (xmlnode.get('fcsapollo') == 'TRUE')
        
        xml_jets = xmlnode.xpath('./jumpjets')
        if xml_jets:
            self += SSWJumpjetList(xml_jets[0])

        xml_legaes = xmlnode.xpath('./leg_aes')
        if xml_legaes:
            self += SSWLegAESList(xml_legaes[0]) 

        for turretXML in xmlnode.xpath('./turret'):
            turret = SSWTurret(turretXML)
            self.append(turret)
        
        for item in xmlnode.xpath('./equipment|./multislot|./arm_aes'):
            item_equip = None
            if item.tag == 'equipment':
                item_equip = SSWEquipment(item, fcs_artemisIV=self.fcs_artemis_iv, fcs_artemisV=self.fcs_artemis_v, fcs_apollo=self.fcs_apollo)
            elif item.tag =='multislot':
                item_equip = SSWMultiSlot(item)
            elif item.tag == 'arm_aes':
                item_equip == None
            else: 
                continue

            self.append(item_equip)
            
            if (self.fcs_artemis_iv and item_equip.equipment.fcs_artemis_iv):
                self.append(SSWAttachedItem('Artemis IV', item_equip, item_type='FCS'))  
            
            if (self.fcs_artemis_v and item_equip.equipment.fcs_artemis_v):
                self.append(SSWAttachedItem('Artemis V', item_equip, item_type='FCS'))  
            
            if (self.fcs_apollo and item_equip.equipment.fcs_apollo):
                self.append(SSWAttachedItem('Apollo', item_equip, item_type='FCS'))    
    
class SSWBaseLoadout(SSWLoadout):
    def __init__(self, xmlnode, motive_type='B'):
        super(SSWBaseLoadout, self).__init__(xmlnode, motive_type=motive_type)
           
        if motive_type == 'B':
            self += SSWBipedActuatorSet( xmlnode.xpath('./actuators')[0] )
        else:
            self += SSWQuadActuatorSet()

class SSWMech(dict):
    def get_number(self, node, xpath):
        text = node.xpath(xpath)[0]
        return int(floor(float(text)))

    def load_baselayout(self, xmlnode):
        self['tonnage'] = xmlnode.get('tons')
        self['mech_name'] = xmlnode.get('name')
        self['mech_code'] = xmlnode.get('model') or '--'
        self['is_omni'] = ( xmlnode.get('omnimech') == 'TRUE' )
        self['motive_type'] = translate.motive_options[ xmlnode.xpath('./motive_type/text()')[0]]
        self['tech_base'] = translate.tech_bases[ xmlnode.xpath('./techbase/text()')[0]]

        self.gyro = SSWGyro( xmlnode.xpath('./gyro')[0] )
        self.engine = SSWEngine( xmlnode.xpath('./engine')[0], gyro_criticals=self.gyro.criticals )
        self.armour = SSWArmour( xmlnode.xpath('./armor')[0] )
        self.structure = SSWStructure( xmlnode.xpath('./structure')[0] )   
        self.cockpit = SSWCockpitSet( xmlnode.xpath('./cockpit')[0] )   
        self.equipment = SSWBaseLoadout( xmlnode.xpath('./baseloadout')[0], motive_type=self['motive_type'])
        
        self.equipment.append(self.gyro)
        self.equipment.append(self.engine)
        self.equipment.append(self.armour)        
        self.equipment.append(self.structure) 
        self.equipment += self.cockpit

        xml_enhancement = xmlnode.xpath('./enhancement')
        if xml_enhancement:
            self.equipment.append(SSWEnhancement(xml_enhancement[0]))

        self.type = xmlnode.xpath('./mech_type/text()')[0]

        self['engine_rating'] = self.engine.rating

    def __init__(self, xmlnode, ssw_filename, production_type='P', base_layout=None):
       
        self['ssw_filename'] = ssw_filename
        self['production_type'] = production_type
        
        if base_layout == None:
            #Omni-mech base layout or Non Omni-mech
            self.load_baselayout(xmlnode) 
            self['omni_loadout'] = 'Base'

            self['production_year'] = self.get_number(xmlnode, './year/text()')
            self['ssw_description'] = xmlnode.xpath('./baseloadout/info/text()')[0]
        else:
            for (key, item) in base_layout.items():
                self[key] = item

            self['omni_loadout'] = xmlnode.get('name')

            self['production_year'] = self.get_number(xmlnode, './loadout_year/text()')
            self['ssw_description'] = xmlnode.xpath('./info/text()')[0]
               
            #Copy all the details from the base_layout        
            self.gyro = base_layout.gyro
            self.engine = base_layout.engine
            self.armour = base_layout.armour
            self.structure = base_layout.structure
            self.cockpit = base_layout.cockpit
            self.type = base_layout.type
            
            self.equipment = SSWLoadout(xmlnode, motive_type=self['motive_type'])
            self.equipment += base_layout.equipment
        
        self['credit_value'] = self.get_number(xmlnode, './cost/text()')
        
        if self['is_omni'] and base_layout == None:
            self['bv_value'] = 0
            
            self.loadouts = [ SSWMech(loadout_node, ssw_filename, production_type= production_type, base_layout=self) for loadout_node in xmlnode.xpath('./loadout') ]
        else:
            self['bv_value'] = self.get_number(xmlnode, './battle_value/text()')
            self.loadouts = []
        
