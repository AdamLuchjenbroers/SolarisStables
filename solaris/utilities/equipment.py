from copy import deepcopy

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
    
    def __iadd__(self, other):
        try:
            for value in other:
                self.add(value)
        except TypeError:
            self.add(other)
        return self
        
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
        
    def extrapolate(self, count):
        start = self['slots'].singleslot()
        
        if start:
            self['slots'].add(start, count)