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

    def test_coredadvance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_cored(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)

    def test_removedadvance(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(stablemech=self.mech)


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
        smw.set_cored(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.chassis)

    def test_chassis_removed(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.chassis)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.chassis)

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
        smw.set_cored(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.config)

    def test_config_removed(self):
        smw = self.mech.weeks.get(stableweek__week__week_number=1, current_design=self.config)
        smw.set_removed(True)
        next_week = self.advanceWeek(self.stable)

        with self.assertRaises(ObjectDoesNotExist, msg='Mech record for cored mech exists after advancing to next week'):
            next_week.mechs.get(current_design=self.config)

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

    
