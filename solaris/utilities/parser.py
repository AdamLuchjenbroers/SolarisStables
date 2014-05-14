from math import floor

from solaris.warbook.mech.models import MechLocation
from solaris.warbook.equipment.models import Equipment

from solaris.utilities import translate 

class SSWMountedItem(dict):

    def mount(self, xmlnode):
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
            
            if loc.text in self.mountings:
                self.mountings[loc.text] += index
            else:
                self.mountings[loc.text] = index
                
        for key in self.mountings:
            self.mountings[key].sort()
            
        if len(self.mountings) == 0:
            self.mountings['--'] = None
    
    def extrapolated(self, criticals):
        if not self.extrapolated:
            loc = self.mountings.keys()[0]
            start = self.mountings[loc][0]
            self.mountings.loc = range(start, start+criticals)

class SSWLocation(dict):
    def __init__(self, mech, armour, code):
        self['mech'] = mech
        self['armour'] = armour
        


class SSWEquipment(SSWMountedItem):
    def __init__(self, xmlnode):
        self['name'] = xmlnode.xpath['./name[1]'].text
        self.node_type = xmlnode.tag
        self['ssw_name'] = '%s - %s' % (self.node_type, self.name)
        
        self.mount(xmlnode)
        
         
class SSWArmour(SSWMountedItem):
    def __init__(self, xmlnode):
         
        #Armour is stored as multiple single-slot assignments, so we can consider
        #it extrapolated already
        self.mount(xmlnode)
        self.extrapolated = True
        
        armorInfo = xmlnode.xpath('./*[not(self::type|self::location)]')
        self.armour = {}
        for location in armorInfo:
            self.armour[location.tag] = int(location.text)
            
        typenode = xmlnode.xpath('./type')
        self.equipment_name = typenode[0].text
        
class SSWEngine(SSWMountedItem):
    def __init__(self, xmlnode):
        self.mountings={'ct' : [1,2,3,8,9,10] }
        self.rating = xmlnode.get('rating')
    
class SSWMech(dict):
    def get_number(self, node, xpath):
        text = node.xpath(xpath)[0]
        return int(floor(float(text)))
    
    def __init__(self, xmlnode, ssw_filename, stock=True):
        self['tonnage'] = xmlnode.get('tons')
        self['mech_name'] = xmlnode.get('name')
        self['mech_code'] = xmlnode.get('model')
        
        self['is_omni'] = ( xmlnode.get('omnimech') == 'TRUE' )
                       
        self['credit_value'] = self.get_number(xmlnode, './cost/text()')
        
        if self['is_omni']:
            self['bv_value'] = 0
        else:
            self['bv_value'] = self.get_number(xmlnode, './battle_value/text()')
        
        self.engine = SSWEngine( xmlnode.xpath('./engine')[0] )
        self.armour = SSWArmour( xmlnode.xpath('./armor')[0] )
        
        self['engine_rating'] = self.engine.rating
        self['stock_design'] = stock
        self['ssw_filename'] = ssw_filename
        
        self['tech_base'] = translate.tech_bases[ xmlnode.xpath('./techbase/text()')[0] ]
        self['motive_type'] = translate.motive_options[ xmlnode.xpath('./motive_type/text()')[0] ]
        
        self.type = xmlnode.xpath('./mech_type/text()')[0]
