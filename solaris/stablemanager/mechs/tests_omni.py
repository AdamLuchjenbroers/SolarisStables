
from django.test import TestCase

from solaris.stablemanager.tests import StableTestMixin

class OmniMechTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.mech = self.addMech(self.stable, mech_name='Owens', mech_code='OW-1', omni_loadout='C') 
        self.base_filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        , 'current_design__omni_loadout' : 'Base'
        }

        self.config_filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        , 'current_design__omni_loadout' : 'C'
        }

    def test_baseChassis(self):
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_baseChassisLoadouts(self):
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 

    def test_configLoaded(self): 
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.config_filter)
        base_smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, base_smw, 'Config_for should refer to the base chassis for the Omnimech')

    def test_nextWeekBaseChassis(self):
        week = self.advanceWeek(self.stable)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_nextWeekBaseChassisLoadouts(self):
        week = self.advanceWeek(self.stable)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 
       
    def test_nextWeekConfigLoaded(self): 
        week = self.advanceWeek(self.stable)
        smw = week.mechs.get(**self.config_filter)
        base_smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, base_smw, 'Config_for should refer to the base chassis for the Omnimech')

class OmniMechLateAddTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.advanceWeek(self.stable)
        self.advanceWeek(self.stable)
        sw = self.stable.get_stableweek(1)

        self.mech = self.addMech(self.stable, stableweek=sw, mech_name='Owens', mech_code='OW-1', omni_loadout='C') 
        self.base_filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        , 'current_design__omni_loadout' : 'Base'
        }

        self.config_filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        , 'current_design__omni_loadout' : 'C'
        }

    def test_baseChassis(self):
        week = self.stable.get_stableweek(2)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_baseChassisLoadouts(self):
        week = self.stable.get_stableweek(2)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 

    def test_configLoaded(self): 
        week = self.stable.get_stableweek(2)
        smw = week.mechs.get(**self.config_filter)
        base_smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, base_smw, 'Config_for should refer to the base chassis for the Omnimech')

    def test_baseChassisWeek3(self):
        week = self.stable.get_stableweek(3)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_baseChassisLoadoutsWeek3(self):
        week = self.stable.get_stableweek(3)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 

    def test_configLoadedWeek3(self): 
        week = self.stable.get_stableweek(3)
        smw = week.mechs.get(**self.config_filter)
        base_smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, base_smw, 'Config_for should refer to the base chassis for the Omnimech')

