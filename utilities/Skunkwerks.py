from math import floor
from lxml import etree

from Validation import expect_integer, expect_alphastring

class SSWFile:
    def __init__(self, sswFileName=None):
        fd = open(sswFileName)
        
        self.xmlFile = etree.parse(fd)
    
    @expect_integer        
    def getCost(self):
        costInfo = self.xmlFile.xpath('/mech/cost')
        return floor( float (costInfo[0].text))        
    
    @expect_integer
    def getBV(self):
        if self.isOmni():
            return 0 # Omnimechs do not store BV values for the base chassis
        else:
            costInfo = self.xmlFile.xpath('/mech/battle_value')
            return costInfo[0].text
        
    @expect_alphastring
    def getType(self):
        typeInfo = self.xmlFile.xpath('/mech/mech_type')
        return typeInfo[0].text
    
    @expect_alphastring
    def getTechBase(self):
        typeInfo = self.xmlFile.xpath('/mech/techbase')
        return typeInfo[0].text
    
    @expect_integer
    def getTonnage(self):
        mechInfo = self.xmlFile.xpath('/mech/@tons')
        return int(mechInfo[0])
    
    def getName(self):
        mechInfo = self.xmlFile.xpath('/mech/@name')
        return mechInfo[0]
    
    def getCode(self):
        mechInfo = self.xmlFile.xpath('/mech/@model')
        return mechInfo[0]
    
    @expect_integer 
    def getEngineRating(self):
        mechInfo = self.xmlFile.xpath('/mech/engine/@rating')
        return int(mechInfo[0])

    def getWalkingMP(self):
        return floor ( self.getEngineRating() / self.getTonnage())
    
    def getArmorType(self):
        pass
    
    def isOmni(self): 
        mechInfo = self.xmlFile.xpath('/mech/@omnimech')
        return mechInfo[0] == "TRUE"