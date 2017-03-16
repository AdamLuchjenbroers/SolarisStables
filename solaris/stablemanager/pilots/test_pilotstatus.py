
from django.test import TestCase

from solaris.stablemanager.tests import StableTestMixin
from . import models

class PilotIsDeadTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.campaign = self.stable.campaign

        self.pilot, self.pilotweek = self.add_pilot(self.stable)

    def test_unharmed(self):
        self.assertFalse(self.pilotweek.is_dead(), 'Unharmed Pilot incorrectly registers as dead')

    def test_nearlydead_wounds(self):
        self.pilotweek.wounds = 5
        self.assertFalse(self.pilotweek.is_dead(), 'Nearly Dead (5 Wounds) Pilot incorrectly registers as dead')

    def test_nearlydead_marks(self):
        self.pilotweek.blackmarks = 5
        self.assertFalse(self.pilotweek.is_dead(), 'Nearly Dead (5 Marks) Pilot incorrectly registers as dead')

    def test_nearlydead_both(self):
        self.pilotweek.wounds = 3
        self.pilotweek.blackmarks = 2
        self.assertFalse(self.pilotweek.is_dead(), 'Nearly Dead (Mixed Wounds / Marks) Pilot incorrectly registers as dead')

    def test_dead_wounds(self):
        self.pilotweek.wounds = 6
        self.assertTrue(self.pilotweek.is_dead(), 'Dead (6 Wounds) Pilot incorrectly registers as alive')

    def test_dead_marks(self):
        self.pilotweek.blackmarks = 6
        self.assertTrue(self.pilotweek.is_dead(), 'Dead (6 Marks) Pilot incorrectly registers as alive')

    def test_dead_both(self):
        self.pilotweek.wounds = 3
        self.pilotweek.blackmarks = 3
        self.assertTrue(self.pilotweek.is_dead(), 'Dead (Mixed Wounds / Marks) Pilot incorrectly registers as alive')

    def test_overdead_wounds(self):
        self.pilotweek.wounds = 7
        self.assertTrue(self.pilotweek.is_dead(), 'Over-dead (7 Wounds) Pilot incorrectly registers as alive')

    def test_overdead_marks(self):
        self.pilotweek.blackmarks = 7
        self.assertTrue(self.pilotweek.is_dead(), 'Over-dead (7 Marks) Pilot incorrectly registers as alive')

    def test_overdead_both(self):
        self.pilotweek.wounds = 4
        self.pilotweek.blackmarks = 4
        self.assertTrue(self.pilotweek.is_dead(), 'Over-dead (Mixed Wounds / Marks) Pilot incorrectly registers as alive')
