
locations_allmechs = (
  ( 'HD', 'Head' )
, ( 'LT', 'Left Torso' )
, ( 'RT', 'Right Torso' )
, ( 'CT', 'Center Torso' )
, ( 'RLT', 'Left Torso (Rear)' )
, ( 'RRT', 'Right Torso (Rear)' )
, ( 'RCT', 'Right Center Torso (Rear)' )
, )

locations_bipedonly = (
  ('RA', 'Right Arm')
, ('LA', 'Left Arm')
, ('RL', 'Right Leg')
, ('LL', 'Left Leg')
, )

locations_biped = locations_allmechs + locations_bipedonly

locations_quadonly = (
, ('RFL', 'Right Fore Leg')
, ('RRL', 'Right Rear Leg')
, ('LFL', 'Left Fore Leg')
, ('RFL', 'Right Fore Leg')
, )

locations_quad = locations_allmechs + locations_quadonly

locations_all = locations_allmechs + locations_quadonly + locations_bipedonly