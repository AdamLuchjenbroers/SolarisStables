from lxml import etree
import os
import re

sswPattern = re.compile('.*\.ssw$')
equipment = set()

def recursiveScanAll(path, relative_path='.'):
    
    for fileName in os.listdir(path):
        fullpath = path + '/' + fileName    
        if os.path.isdir(fullpath):
            recursiveScanAll(fullpath, relative_path=relative_path + '/' + fileName)
            
        if os.path.isfile(fullpath) and sswPattern.match(fileName):
            getEquipmentList(fullpath)
    
def getEquipmentList(sswFileName):
    
    fd = open(sswFileName)
    xmlFile = etree.parse(fd)
    
    if xmlFile.xpath('/mech/techbase')[0].text != 'Inner Sphere':
        return
    
    if xmlFile.xpath('/mech/mech_type')[0].text != 'BattleMech':
        return    
    
    for item in xmlFile.xpath('//equipment/name[text()]'):
        item_name = item.text
        if item_name[0:3] in ('(T)', '(R)'):
            item_name = item_name[4:]
            
        if item_name[0] == '@':
            item_type = 'Ammo'
        else:
            item_type = 'Equipment'
        
        equipment.add('%s - %s' % (item_type, item_name))
            
    
    
if __name__ == '__main__':
    
    basepath = '/home/notavi/Programming/SourceData/SSW_Master'
    
    recursiveScanAll(basepath)
    
    equip_list = list(equipment)
    equip_list.sort()
    
    for item in equip_list:
        print item
    