locations_all = {
    'hd': 'HD',
    'rt': 'RT',
    'rtr' : 'RRT',
    'lt' : 'LT',
    'ltr' : 'RLT',
    'ct' : 'CT',
    'ctr' : 'RCT',
    'ra' : 'RA',
    'la' : 'LA',
    'll' : 'LL',
    'rl' : 'RL',
    '--' : '--',
}

locations_biped = locations_all.copy()
locations_biped['ra'] = 'RA'
locations_biped['la'] = 'LA'
locations_biped['ll'] = 'LL'
locations_biped['rl'] = 'RL'

locations_quad = locations_all.copy()
locations_quad['ra'] = 'RFL'
locations_quad['la'] = 'LFL'
locations_quad['ll'] = 'LRL'
locations_quad['rl'] = 'RRL'
locations_quad['frl'] = 'RFL'
locations_quad['fll'] = 'LFL'
locations_quad['rrl'] = 'LRL'
locations_quad['rll'] = 'RRL'

tech_bases = {
    'Inner Sphere' : 'I'
,   'Clan' : 'C'
,   'Mixed' : 'M'
}

motive_options = {
    'Biped' : 'B'
,   'Quad'  : 'Q'
}