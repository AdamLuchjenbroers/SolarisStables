
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

    def test_baseChassisWeek1(self):
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_baseChassisLoadoutsWeek1(self):
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 

    def test_configLoadedWeek1(self): 
        week = self.stable.get_stableweek(1)
        smw = week.mechs.get(**self.config_filter)
        base_smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, base_smw, 'Config_for should refer to the base chassis for the Omnimech')

    def test_baseChassisWeek2(self):
        week = self.stable.get_stableweek(2)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.config_for, None, 'Config_for should not be populated for base chassis') 

    def test_baseChassisLoadoutsWeek2(self):
        week = self.stable.get_stableweek(2)
        smw = week.mechs.get(**self.base_filter)
        self.assertEquals(smw.loadouts.count(), 1, 'Base loadout should have 1 available config, found %d' % smw.loadouts.count()) 

    def test_configLoadedWeek2(self): 
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

class OmniMechPurchaseTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        sw = self.stable.get_stableweek()

        self.mech = [
            self.addMech(self.stable, stableweek=sw, mech_name='Owens', mech_code='OW-1', omni_loadout='C') 
        ,   self.addMech(self.stable, stableweek=sw, mech_name='Owens', mech_code='OW-1', omni_loadout='A') 
        ]
        self.filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        }
        

    def test_stableMechIsBaseConfig(self):
        self.assertEquals(self.mech[0].purchased_as.omni_loadout,'Base','create_mech should return the Base config when adding Omnimechs')

    def test_sameBaseMech(self):
        self.assertEquals(self.mech[0],self.mech[1],'Base mech should be identical for both Omni-mech configs')

    def test_firstLedgerCost(self):
        week = self.stable.get_stableweek()
        smw = week.mechs.get(current_design__omni_loadout='C', **self.filter)
        ledger = week.entries.get(ref_stablemech_week=smw)
        
        self.assertEquals(-ledger.cost, 7929281, 'A New Owens OW1 (C) should cost 7929281, costed %d' % -ledger.cost)

    def test_baseHasTwoLoadouts(self):
        week = self.stable.get_stableweek()
        smw = week.mechs.get(current_design__omni_loadout='Base', **self.filter)
        
        self.assertEquals(smw.loadouts.count(), 2, 'Owens OW-1 (Base) should have 2 attached configs, found %d' % smw.loadouts.count())

    def test_firstLedgerDescription(self):
        week = self.stable.get_stableweek()
        smw = week.mechs.get(current_design__omni_loadout='C', **self.filter)
        ledger = week.entries.get(ref_stablemech_week=smw)
        
        expect_description = 'Purchase - Owens OW-1 (C)'
        self.assertEquals(ledger.description, expect_description, 'Purchase Description Incorrect, expected %s found %s' % (expect_description, ledger.description))        

    def test_secondLedgerCost(self):
        week = self.stable.get_stableweek()
        smw = week.mechs.get(current_design__omni_loadout='A', **self.filter)
        ledger = week.entries.get(ref_stablemech_week=smw)
        
        self.assertEquals(-ledger.cost, 149850, 'An additional Owens OW-1 (A) config should cost 149850, costed %d' % -ledger.cost)

    def test_secondLedgerDescription(self):
        week = self.stable.get_stableweek()
        smw = week.mechs.get(current_design__omni_loadout='A', **self.filter)
        ledger = week.entries.get(ref_stablemech_week=smw)
        
        expect_description = 'New Loadout - Owens OW-1 (A)'
        self.assertEquals(ledger.description, expect_description, 'Purchase Description Incorrect, expected %s found %s' % (expect_description, ledger.description))    

class OmniMechRemovalTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        sw = self.stable.get_stableweek()

        self.mech = [
            self.addMech(self.stable, stableweek=sw, mech_name='Owens', mech_code='OW-1', omni_loadout='C') 
        ,   self.addMech(self.stable, stableweek=sw, mech_name='Owens', mech_code='OW-1', omni_loadout='A') 
        ]
        self.filter = {
          'current_design__mech_name' : 'Owens'
        , 'current_design__mech_code' : 'OW-1'
        }

    def test_countChassisAndConfig(self):
        sw = self.stable.get_stableweek()
        count = sw.mechs.filter(current_design__mech_name='Owens', current_design__mech_code='OW-1').count()

        self.assertEquals(count, 3, 'Expected 3 StableMechs (Chassis + 2 Configs), found %i' % count)

    def test_removeConfig(self):
        sw = self.stable.get_stableweek()
        config = sw.mechs.get(current_design=self.mech[1].purchased_as)

        config.set_removed(True)

        self.assertFalse(config.removed, 'Omnimech config not tagged as removed')

    def test_removeChassisStays(self):
        sw = self.stable.get_stableweek()
        config = sw.mechs.get(current_design=self.mech[1].purchased_as)

        config.set_removed(True)

        chassis = sw.mechs.get(current_design=self.mech[0].purchased_as.omni_basechassis)
        self.assertTrue(chassis.removed, 'Omnimech base chassis incorrectly removed')

    def test_removeOtherConfigStays(self):
        sw = self.stable.get_stableweek()
        config = sw.mechs.get(current_design=self.mech[1].purchased_as)

        config.set_removed(True)

        other = sw.mechs.get(current_design=self.mech[0].purchased_as)
        self.assertTrue(other.removed, 'Omnimech base chassis incorrectly removed')
