from math import floor
from lxml import etree

from solaris.utilities.validation import expect_integer, expect_alphastring

class SSWEquipment:
    def __init__(self, xmlnode):
        self.equipment_name = xmlnode.text
        self.type = xmlnode.tag
        
        locations = xmlnode.xpath('./location')
        
        self.mountings = {}
        for loc in locations:
            if loc.text in self.mountings:
                self.mountings[loc.text].append(int(location.get('index')))
            else:
                self.mountings[loc.text] = [int(location.get('index'))]
                
       for key in self.mountings:
            self.mountings[key].sort()
            
       if len(self.mountings) == 0
           self.mountings['--'] = None
         
class SSWArmour(SSWEquipment):
    def __init__(self, xmlnode):
        super(SSWArmour,self).__init__(xmlnode)
    
        armorInfo = xmlnode.xpath('./*[not(self::type|self::location)]')
        self.armor = {}
        for location in armorInfo:
            armor[location.tag] = int(location.text)
            
        typenode = xmlnode.xpath('./type')
        self.equipment_name = typenode[0].text
    
        

class SSWFile:
    def __init__(self, sswFileName=None):
        fd = open(sswFileName)
        self.file_name = sswFileName
        
        self.xmlFile = etree.parse(fd)
    
    @expect_integer        
    def get_cost(self):
        costInfo = self.xmlFile.xpath('/mech/cost')
        return floor( float (costInfo[0].text))        
    
    @expect_integer
    def get_cost(self):
        if self.isOmni():
            return 0 # Omnimechs do not store BV values for the base chassis
        else:
            costInfo = self.xmlFile.xpath('/mech/battle_value')
            return costInfo[0].text
        
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