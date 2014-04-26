import libxml2
from math import floor

class SSWFile:
    def __init__(self, sswFileName=None):
        self.xmlFile = libxml2.parseFile(sswFileName)
        
        self.xpathContext = self.xmlFile.xpathNewContext()
            
    def getCost(self):
        costInfo = self.xpathContext.xpathEval('/mech/cost')
        return floor( float (costInfo[0].getContent()))        
    
    def getBV(self):
        if self.isOmni():
            return 0 # Omnimechs do not store BV values for the base chassis
        else:
            costInfo = self.xpathContext.xpathEval('/mech/battle_value')
            return int (costInfo[0].getContent())
        
    def getType(self):
        typeInfo = self.xpathContext.xpathEval('/mech/mech_type')
        return typeInfo[0].getContent()
    
    def getTechBase(self):
        typeInfo = self.xpathContext.xpathEval('/mech/techbase')
        return typeInfo[0].getContent()
    
    def getTonnage(self):
        mechInfo = self.xpathContext.xpathEval('/mech/@tons')
        return int(mechInfo[0].getContent())
    
    def getName(self):
        mechInfo = self.xpathContext.xpathEval('/mech/@name')
        return mechInfo[0].getContent()
    
    def getCode(self):
        mechInfo = self.xpathContext.xpathEval('/mech/@model')
        return mechInfo[0].getContent()
     
    def getEngineRating(self):
        mechInfo = self.xpathContext.xpathEval('/mech/engine/@rating')
        return int(mechInfo[0].getContent())

    def getWalkingMP(self):
        return floor ( self.getEngineRating() / self.getTonnage())
    
    def isOmni(self): 
        mechInfo = self.xpathContext.xpathEval('/mech/@omnimech')
        return mechInfo[0].getContent() == "TRUE"