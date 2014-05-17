
class CriticalsList(object):
    def __init__(self, criticals=None):
        if criticals and isinstance(criticals, list):
            criticals.sort()
            self.slots = criticals
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
        
    def __add__(self, other):
        # Attempt to iterate over it, if that values assume it's a single value
        try:
            for value in other:
                self.add(value)
        except TypeError:
            self.add(other)