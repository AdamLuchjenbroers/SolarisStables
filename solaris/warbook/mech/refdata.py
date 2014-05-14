
locations_allmechs = (
  ( 'HD', 'Head' )
, ( 'LT', 'Left Torso' )
, ( 'RT', 'Right Torso' )
, ( 'CT', 'Center Torso' )
, ( 'RLT', 'Left Torso (Rear)' )
, ( 'RRT', 'Right Torso (Rear)' )
, ( 'RCT', 'Center Torso (Rear)' )
, ( '--', 'No Location' )
)

locations_bipedonly = (
  ('RA', 'Right Arm')
, ('LA', 'Left Arm')
, ('RL', 'Right Leg')
, ('LL', 'Left Leg')
)

locations_biped = locations_allmechs + locations_bipedonly

locations_quadonly = (
  ('RFL', 'Right Fore Leg')
, ('RRL', 'Right Rear Leg')
, ('LFL', 'Left Fore Leg')
, ('LRL', 'Left Rear Leg')
)

locations_quad = locations_allmechs + locations_quadonly

locations_all = locations_allmechs + locations_quadonly + locations_bipedonly

structure = {          
  20  : { 'head' : 3, 'arm' :  3, 'leg' :  4, 'sidetorso' :  5, 'centertorso' :  6},
  25  : { 'head' : 3, 'arm' :  4, 'leg' :  6, 'sidetorso' :  6, 'centertorso' :  8},
  30  : { 'head' : 3, 'arm' :  5, 'leg' :  7, 'sidetorso' :  7, 'centertorso' : 10},
  35  : { 'head' : 3, 'arm' :  6, 'leg' :  8, 'sidetorso' :  8, 'centertorso' : 11},
  40  : { 'head' : 3, 'arm' :  6, 'leg' : 10, 'sidetorso' : 10, 'centertorso' : 12},
  45  : { 'head' : 3, 'arm' :  7, 'leg' : 11, 'sidetorso' : 11, 'centertorso' : 14},
  50  : { 'head' : 3, 'arm' :  8, 'leg' : 12, 'sidetorso' : 12, 'centertorso' : 16},
  55  : { 'head' : 3, 'arm' :  9, 'leg' : 13, 'sidetorso' : 13, 'centertorso' : 18},
  60  : { 'head' : 3, 'arm' : 10, 'leg' : 14, 'sidetorso' : 14, 'centertorso' : 20},
  65  : { 'head' : 3, 'arm' : 10, 'leg' : 15, 'sidetorso' : 15, 'centertorso' : 21},
  70  : { 'head' : 3, 'arm' : 11, 'leg' : 15, 'sidetorso' : 15, 'centertorso' : 22},
  75  : { 'head' : 3, 'arm' : 12, 'leg' : 16, 'sidetorso' : 16, 'centertorso' : 23},
  80  : { 'head' : 3, 'arm' : 13, 'leg' : 17, 'sidetorso' : 17, 'centertorso' : 25},
  85  : { 'head' : 3, 'arm' : 14, 'leg' : 18, 'sidetorso' : 18, 'centertorso' : 27},
  90  : { 'head' : 3, 'arm' : 15, 'leg' : 19, 'sidetorso' : 19, 'centertorso' : 29},
  95  : { 'head' : 3, 'arm' : 16, 'leg' : 20, 'sidetorso' : 20, 'centertorso' : 30},
  100 : { 'head' : 3, 'arm' : 17, 'leg' : 21, 'sidetorso' : 21, 'centertorso' : 31},
}

def is_leg(location):
    return location in ('LL', 'RL', 'RFL', 'LFL', 'RRL', 'LRL')

def is_arm(location):
    return location in ('LA', 'RA')

def is_sidetorso(location):
    return location in ('RT', 'LT')

def is_centertorso(location):
    return location == 'CT'

def is_head(location):
    return location == 'HD'

def is_rear(location):
    return location in ('RRT', 'RLT', 'RCT')

def structure_entry(location):
    if is_arm(location):
        return 'arm'
    elif is_leg(location):
        return 'leg'
    elif is_sidetorso(location):
        return 'sidetorso'
    elif is_centertorso(location):
        return 'centertorso'
    elif is_head(location):
        return 'head'
    else:
        return 'other'
    
    

def criticals(location):
    if is_head(location) or is_leg(location):
        return 6
    if location == '--' or is_rear(location):
        return 0
    return 12
