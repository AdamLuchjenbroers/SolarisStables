
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

def criticals(location):
    if is_head(location) or is_leg(location):
        return 6
    if location == '--' or is_rear(location):
        return 0
    return 12
