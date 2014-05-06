from math import floor
from lxml import etree

from solaris.utilities.validation import expect_integer, expect_alphastring

class SSWEquipment(dict):
    def __init__(self, xmlnode):
        self.name = xmlnode.xpath['./name[1]'].text
        self.node_type = xmlnode.tag
        self.ssw_name = '%s - %s' % (self.node_type, self.name)
        
        locations = xmlnode.xpath('./location|./splitlocation')
        
        #Most entries only record a single slot, and require that we 
        #extrapolate from there.
        self.extrapolated = False
        
        self.mountings = {}
        for loc in locations:
            if loc.tag == 'location':
                index = [int(locations.get('index'))+1]
            if loc.tag == 'splitlocation':
                count = int(locations.get('number'))
                start = int(locations.get('index'))
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
         
class SSWArmour(SSWEquipment):
    def __init__(self, xmlnode):
        super(SSWArmour,self).__init__(xmlnode)
    
        armorInfo = xmlnode.xpath('./*[not(self::type|self::location)]')
        self.armor = {}
        for location in armorInfo:
            self.armor[location.tag] = int(location.text)
            
        typenode = xmlnode.xpath('./type')
        self.equipment_name = typenode[0].text
        
class SSWEngine(SSWEquipment):
    def __init__(self, xmlnode):
        self.mountings={'ct' : [1,2,3,8,9,10] }
        self.rating = xmlnode.get('rating')
    
class SSWMech(dict):
    def __init__(self, xmlnode):
        self['tonnage'] = int(xmlnode.get('tons'))
        self['mech_name'] = xmlnode.get('name')
        self['mech_code'] = xmlnode.get('model')
        
        self['is_omni'] = ( xmlnode.get('omni') == 'TRUE' )
               
        self['credit_cost'] = int(floor(xmlnode.xpath('./cost')[0]))
        
        if self['is_omni']:
            self['bv_cost'] = 0
        else:
            self['bv_cost'] = int(floor(xmlnode.xpath('./battle_value')[0]))
        
        self.engine = SSWEngine( xmlnode.xpath('./engine')[0] )
        self['engine_rating'] = self.engine.rating
        
        self.armour = SSWArmour( xmlnode.xpath('./armor')[0] )
        
        self.equipment = []
        for node in xmlnode.xpath('./baselayout/*/equipment'):
            self.equipment.add( SSWEquipment(node) )
           
        

class SSWFile:
    def __init__(self, sswFileName=None):
        fd = open(sswFileName)
        self.file_name = sswFileName
        
        self.xmlFile = etree.parse(fd)
        self.mech = SSWMech( self.xmlFile.xpath('/mech')[0] )
    
    @expect_integer        
    def get_cost(self):
        return self.mech.credit_cost        
    
    @expect_integer
    def get_bv(self):
        return self.mech.bv_cost
        
    @expect_alphastring
    def get_type(self):
        typeInfo = self.xmlFile.xpath('/mech/mech_type')
        return typeInfo[0].text
    
    @expect_alphastring
    def get_techbase(self):
        typeInfo = self.xmlFile.xpath('/mech/techbase')
        return typeInfo[0].text
        
    @expect_alphastring
    def get_motive_type(self):
        mtNodes = self.xmlFile.xpath('/mech/motive_type')
        return mtNodes[0].text
    
    @expect_integer
    def get_tonnage(self):
        mechInfo = self.xmlFile.xpath('/mech/@tons')
        return int(mechInfo[0])
    
    def get_name(self):
        mechInfo = self.xmlFile.xpath('/mech/@name')
        return mechInfo[0]
    
    def get_code(self):
        mechInfo = self.xmlFile.xpath('/mech/@model')
        return mechInfo[0]
    
    @expect_integer 
    def get_enginerating(self):
        mechInfo = self.xmlFile.xpath('/mech/engine/@rating')
        return int(mechInfo[0])

        
    def get_armour(self):
        armour_node = self.xmlFile.xpath('/mech/armor')[0]
        return SSWArmour(armour_node)
        
    def is_omni(self): 
        mechInfo = self.xmlFile.xpath('/mech/@omnimech')
        return mechInfo[0] == "TRUE"