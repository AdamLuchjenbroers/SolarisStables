from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

from solaris.stablemanager.tests import StableTestMixin

class MechAdvanceTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.stable.campaign.current_week().advance()
        self.mech = self.addMech(self.stable, mech_name='Wolverine', mech_code='WVR-7D')

    def test_mechadvance(self):
        next_week = self.advanceWeek(self.stable)

        try:
            next_week.mechs.get(stablemech=self.mech)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_mechadvance_status(self):
        next_week = self.advanceWeek(self.stable)

        try:
            mech = next_week.mechs.get(stablemech=self.mech)
            self.assertEquals(mech.mech_status, 'O', 'Expected Advanced Mech to have status: O, got status %s' % mech.mech_status) 
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_cored_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.core_mech(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_removed_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for removed mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_hidden_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_status('-')
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for hidden mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_honoured_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_status('D')
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for display mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_auction_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_status('A')
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for auctioned mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_reinstatement(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_status('R')
        next_week = self.advanceWeek(self.stable)

        smw.set_status('O')
        try:
            next_week.mechs.get(stablemech=self.mech)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after reinstatement.')

    def test_reinstatement_status(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_status('R')
        next_week = self.advanceWeek(self.stable)

        smw.set_status('O')
        try:
            mech = next_week.mechs.get(stablemech=self.mech)
            self.assertEquals(mech.mech_status, 'O', 'Expected Reinstated Mech to have status: O, got status %s' % mech.mech_status) 
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after reinstatement')

class OmnimechAdvanceTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.stable.campaign.current_week().advance()
        self.mech = self.addMech(self.stable, mech_name='Owens', mech_code='OW-1', omni_loadout='Prime')

        self.chassis = self.mech.purchased_as
        self.config = self.chassis.loadouts.get(omni_loadout='Prime') 

    def test_chassis_advance(self):
        next_week = self.advanceWeek(self.stable)

        try:
            next_week.mechs.get(current_design=self.chassis)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_chassis_cored(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.chassis)
        smw.core_mech(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.chassis)

    def test_chassis_removed(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.chassis)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.chassis)

    def test_chassis_reinstated(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.chassis)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        smw.set_removed(False)

        #TODO: Fix for sync issue, remove after migration to Django 1.8+
        next_week = self.stable.get_stableweek(2)
        try:
            mech = next_week.mechs.get(stablemech=self.mech, current_design=self.chassis)
            self.assertEquals(mech.mech_status, 'O', 'Expected Reinstated Mech to have status: O, got status %s' % mech.mech_status) 
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after reinstatement')

    def test_chassis_has_config(self):
        next_week = self.advanceWeek(self.stable)

        try:
            chassisweek = next_week.mechs.get(current_design=self.chassis)
            chassisweek.loadouts.get(current_design=self.config)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_config_advance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.config)
        next_week = self.advanceWeek(self.stable)

        try:
            next_week.mechs.get(current_design=self.config)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_config_cored(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.config)
        smw.core_mech(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.config)

    def test_config_removed(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.config)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.config)

    def test_config_reinstated(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.chassis)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        smw.set_removed(False)
        try:
            mech = next_week.mechs.get(stablemech=self.mech, current_design=self.config)
            self.assertEquals(mech.mech_status, 'O', 'Expected Reinstated Mech to have status: O, got status %s' % mech.mech_status) 
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after reinstatement')

    def test_config_has_chassis(self):
        next_week = self.advanceWeek(self.stable)

        try:
            configweek = next_week.mechs.get(current_design=self.config)
            chassis = configweek.config_for.current_design

            self.assertEqual(chassis, self.chassis, 'Base config incorrect after advancing (%s)' % chassis)
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_advance_sameweek(self):
        next_week = self.advanceWeek(self.stable)

        try:
            chassisweek = next_week.mechs.get(current_design=self.chassis)
            configweek = chassisweek.loadouts.get(current_design=self.config)
            self.assertEqual(chassisweek.stableweek, configweek.stableweek, 'Omnimech loadout stableweek doesn\'t match parent config')
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Mech Record Missing after advancing to next week')

    def test_config_advance_after(self):
        first_week = self.stable.get_stableweek(1)    
        next_week = self.advanceWeek(self.stable)

        # TODO: Clean-up re-fetching after upgrade to Django 1.8+
        new_config = self.addMech(self.stable, stableweek=self.stable.get_stableweek(1), mech_name='Owens', mech_code='OW-1', omni_loadout='D')
        try:
            chassisweek = next_week.mechs.get(current_design=self.chassis)
            configweek = chassisweek.loadouts.get(current_design__omni_loadout='D')
        except ObjectDoesNotExist:
            self.assertFalse(True, 'Newly added config not found in later weeks')

class LateAdditionTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.stable.campaign.current_week().advance()

        self.first_week = self.stable.get_stableweek(1)
        self.stableweek = self.first_week.advance()

    def test_add_basic(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Wolverine', mech_code='WVR-7D')

        exists = self.stableweek.mechs.filter(stablemech=mech).exists()
        self.assertTrue(exists, 'Mech failed to advance to next week')

    def test_add_basic_status(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Wolverine', mech_code='WVR-7D')

        mech = self.stableweek.mechs.get(stablemech=mech)
        self.assertEquals(mech.mech_status, 'O', 'Late added mech has incorrect status code, expected O, found %s' % mech.mech_status)

    def test_add_omni_chassis(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Owens', mech_code='OW-1', omni_loadout='Prime')

        exists = self.stableweek.mechs.filter(stablemech=mech, current_design__omni_loadout='Base').exists()
        self.assertTrue(exists, 'Omnimech failed to advance to next week')

    def test_add_omni_chassis_status(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Owens', mech_code='OW-1', omni_loadout='Prime')

        mech = self.stableweek.mechs.get(stablemech=mech, current_design__omni_loadout='Base')
        self.assertEquals(mech.mech_status, 'O', 'Omnimech config has incorrect status code, expected O, found %s' % mech.mech_status)

    def test_add_omni_config(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Owens', mech_code='OW-1', omni_loadout='Prime')

        exists = self.stableweek.mechs.filter(stablemech=mech, current_design__omni_loadout='Prime').exists()
        self.assertTrue(exists, 'Omnimech config failed to advance to next week')

    def test_add_omni_config_status(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Owens', mech_code='OW-1', omni_loadout='Prime')

        mech = self.stableweek.mechs.get(stablemech=mech, current_design__omni_loadout='Prime')
        self.assertEquals(mech.mech_status, 'O', 'Omnimech config has incorrect status code, expected O, found %s' % mech.mech_status)

    def test_remove_after_add(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Wolverine', mech_code='WVR-7D')

        mechweek = self.first_week.mechs.get(stablemech=mech)
        mechweek.set_removed(True)

        mechweek = self.stableweek.mechs.get(stablemech=mech)
        self.assertEquals(mechweek.mech_status, '-', 'Removed mech has incorrect status code, expected -, found %s' % mechweek.mech_status)

    def test_delivery(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Wolverine', mech_code='WVR-7D')

        mechweek = self.first_week.mechs.get(stablemech=mech)
        mechweek.delivery = 2
        mechweek.save()

        mechweek = self.stableweek.mechs.get(stablemech=mech)
        self.assertEquals(mechweek.delivery, 1, 'Delivery value for following week incorrect, expected 1, found %i' % mechweek.delivery)
   
    def test_reinstatement(self):
        mech = self.addMech(self.stable, stableweek=self.first_week, mech_name='Wolverine', mech_code='WVR-7D')

        mechweek = self.first_week.mechs.get(stablemech=mech)
        mechweek.set_removed(True)
        mechweek.set_removed(False)

        mechweek = self.stableweek.mechs.get(stablemech=mech)
        self.assertEquals(mechweek.mech_status, 'O', 'Reinstated mech has incorrect status code, expected O, found %s' % mechweek.mech_status)
