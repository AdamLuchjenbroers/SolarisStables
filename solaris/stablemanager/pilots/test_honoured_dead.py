
from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

from solaris.stablemanager.tests import StableTestMixin

import json

from . import models

class HonouredDeadCreationTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.campaign = self.stable.campaign

        self.pilot, self.pilotweek = self.add_pilot(self.stable)

    def test_alive_pilot(self):
        hd = self.pilotweek.honour_dead()
        self.assertEquals(hd, None, 'Expected honour_dead() to return None for an alive pilot, got %s' % hd)

    def test_dead_pilot(self):
        self.pilotweek.wounds = 6
        hd = self.pilotweek.honour_dead()
        self.assertIsInstance(hd, models.HonouredDead, 'Expected honour_dead() to return HonouredDead object for a dead pilot, got %s' % hd)

class HonouredDeadBasicTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.campaign = self.stable.campaign

        self.pilot, self.first_pw = self.add_pilot(self.stable)

        self.first_pw.wounds = 6
        self.first_pw.save() 

    def test_add_honoured(self):
        self.first_pw.honour_dead()
        sw = self.stable.get_stableweek()

        try:
            models.HonouredDead.objects.get(pilot = self.pilot, week=sw) 
        except models.HonouredDead.DoesNotExist:
            hdl = '\nPresent Honoured Dead:\n'
            for hd in models.HonouredDead.objects.all():
                hdl += '\t* Pilot %s, Week %s\n' % (hd.pilot, hd.week)
            self.assertFalse(True, 'Failed to add Honoured Dead record to week %s, pilot %s%s' % (sw, self.pilot, hdl))

    def test_add_honoured_return(self):
        hd = self.first_pw.honour_dead()

        self.assertIsInstance(hd, models.HonouredDead, 'honour_dead() does not return an Honoured Dead object, instead returned %s' % hd)

    def test_add_honoured_return_hasvalue(self):
        hd = self.first_pw.honour_dead()

        self.assertNotEquals(hd, None, 'honour_dead() returned no value')

    def test_add_honoured_week(self):
        hd = self.first_pw.honour_dead()

        self.assertEquals(hd.week, self.first_pw.week, 'Honoured Dead Week does not match source Pilot Week value, %s != %s' % (hd.week, self.first_pw.week))

    def test_add_honoured_pilot(self):
        hd = self.first_pw.honour_dead()

        self.assertEquals(hd.pilot, self.first_pw.pilot, 'Honoured Dead Pilot does not match source Pilot Week value, %s != %s' % (hd.pilot, self.first_pw.pilot))

    def test_remove_honoured(self):
        hd = self.first_pw.honour_dead()

        self.assertFalse(self.first_pw.removed, 'Pilot not removed from stable after being honoured as dead')

    def test_is_honoured(self):
        hd = self.first_pw.honour_dead()

        # Refetch to address ORM de-sync issue
        # TODO: Clean this up after upgrading to Django 1.8+
        pw = self.pilot.weeks.get(id=self.first_pw.id)
        self.assertTrue(pw.is_honoured(), 'is_honoured() failed to confirm pilot was honoured dead')

    def test_is_honoured_pre(self):
        # Test before honouring the pilot as dead to confirm that this method returns the correct value.
        self.assertFalse(self.first_pw.is_honoured(), 'is_honoured() incorrectly returns True')

    def test_fame_value(self):
        hd = self.first_pw.honour_dead()
        self.assertEquals(hd.fame_value(), 1, 'fame_value() returns incorrect fame value, expected 1 got %i' % hd.fame_value())

    def test_honoured_removal(self):
        hd = self.first_pw.honour_dead()
        hd.delete()

        self.assertFalse(self.first_pw.is_honoured(), 'Pilot still registers as honoured after honours removed')
         

class HonouredDeadMechTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.campaign = self.stable.campaign

        self.pilot, self.first_pw = self.add_pilot(self.stable, wounds=6)
        self.mech = self.addMech(self.stable, mech_name='Wolverine', mech_code='WVR-7D')

        smw = self.mech.weeks.get(stableweek=self.stable.get_stableweek(1))
        smw.signature_of = self.pilot
        smw.save()

        self.honours = self.first_pw.honour_dead(display_mech = self.mech)

    def test_is_honoured(self):
        # Refetch to address ORM de-sync issue
        # TODO: Clean this up after upgrading to Django 1.8+
        pw = self.pilot.weeks.get(id=self.first_pw.id)
        self.assertTrue(pw.is_honoured(), 'is_honoured() failed to confirm pilot was honoured dead')

    def test_display_mech(self):
        expect = self.mech
        result = self.honours.display_mech

        self.assertEquals(expect, result, 'DisplayMech is incorrect, expected %s, got %s' % (expect, result))

    def test_fame_value(self):
        self.assertEquals(self.honours.fame_value(), 2, 'fame_value() returns incorrect fame value, expected 2 got %i' % self.honours.fame_value())

    def test_mech_status(self):
        smw = self.mech.weeks.get(stableweek=self.stable.get_stableweek(1))

        self.assertEquals(smw.mech_status, 'D', 'Mech status should indicate mech is on display (D), instead got status: %s' % smw.mech_status)

    def test_removal_update_mech(self):
        self.honours.delete()
        smw = self.mech.weeks.get(stableweek=self.stable.get_stableweek(1))

        self.assertEquals(smw.mech_status, 'O', 'Mech status should indicate mech is operational (O), instead got status: %s' % smw.mech_status)

class HonouredDeadAdvanceTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()
        self.campaign = self.stable.campaign

        n = self.campaign.current_week().advance()

        self.pilot, self.first_pw = self.add_pilot(self.stable, wounds=6) 

    def get_first_pw(self):
        #Re fetch Pilotweek to avoid an ORM de-sync issue
        #TODO: Clean this up after upgrading to Django 1.8+
        first_sw = self.stable.get_stableweek(1)
        return first_sw.pilots.get(id=self.first_pw.id)
    

    def test_manual_advance_return(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        second_hd = hd.cascade_advance()
        self.assertNotEquals(second_hd, None, 'cascade_advance() did not return an honoured dead reference')

    def test_manual_advance(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        second_hd = hd.cascade_advance()
        self.assertEquals(second_hd.week, sw, 'Honoured Dead Incorrectly Advanced: %s != %s' % (second_hd.week, sw))

    def test_advance_after_add(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        self.assertNotEqual(hd.next_week, None, 'Honoured dead record for next week missing after add')

    def test_advance_after_add_check_week(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        self.assertEqual(hd.next_week.week, sw, 'Honoured dead record for for next week has incorrect link to %s' % hd.next_week.week)

    def test_advance_after_add_check_pilot(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        self.assertEqual(hd.next_week.pilot, self.pilot, 'Honoured dead record for for next week has incorrect link to pilot %s' % hd.next_week.pilot)
       
    def test_advance_after_add_query(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()
       
        try:
            models.HonouredDead.objects.get(pilot=self.pilot, week=sw) 
        except models.HonouredDead.DoesNotExist:
            self.assertFalse(True, 'Honoured Dead record not added to subsequent week %s' % sw)

    def test_auto_advance(self):
        self.first_pw.honour_dead()
        sw = self.stable.get_stableweek().advance()
       
        try:
            models.HonouredDead.objects.get(pilot=self.pilot, week=sw) 
        except models.HonouredDead.DoesNotExist:
            self.assertFalse(True, 'Honoured Dead record missing after advance to week %s' % sw)

    def test_removal(self):
        hd = self.get_first_pw().honour_dead()
        hd.delete()

        qs = models.HonouredDead.objects.filter(pilot=self.pilot)
        self.assertEquals(qs.count(), 0, 'Expected no HonouredDead records for pilot, found %d' % qs.count())

    def test_cascade_removal(self):
        sw = self.stable.get_stableweek().advance()
        hd = self.get_first_pw().honour_dead()

        hd.delete()

        qs = models.HonouredDead.objects.filter(pilot=self.pilot)
        self.assertEquals(qs.count(), 0, 'Expected no HonouredDead records for pilot, found %d' % qs.count())

    def test_removal_leavebefore(self):
        self.stable.get_stableweek().advance()

        hd = self.get_first_pw().honour_dead()
        hd.next_week.delete()

        # Re-fetch from Database due to ORM de-sync issues
        # TODO: Clean this up after migrating to Django 1.8+
        hd = models.HonouredDead.objects.get(id=hd.id)
        self.assertTrue(hd.removed, 'Previous week not marked as removed')      
       

class HonouredDeadWebTests(StableTestMixin, TestCase):
    def setUp(self):
        self.stable = self.createStable()

        self.client = Client()
        self.client.login(username='test-user', password='pass')

        self.pilot, self.first_pw = self.add_pilot(self.stable, wounds=6) 

    def test_add_http_response(self):
        formdata = {'callsign' : self.pilot.pilot_callsign} 
        response = self.client.post('/stable/pilots/1/honoured-dead/add', formdata)

        self.assertEqual(response.status_code, 200, 'HTTP Post request to Add Honoured Dead failed with error (HTTP %s: %s)' \
           % (response.status_code, response.content))

    def test_add_honoured(self):
        sw = self.stable.get_stableweek()

        formdata = {'callsign' : self.pilot.pilot_callsign} 

        self.client.post('/stable/pilots/1/honoured-dead/add', formdata)

        try:
            models.HonouredDead.objects.get(pilot = self.pilot, week=sw) 
        except models.HonouredDead.DoesNotExist:
            hdl = '\nPresent Honoured Dead:\n'
            for hd in models.HonouredDead.objects.all():
                hdl += '\t* Pilot %s, Week %s\n' % (hd.pilot, hd.week)
            self.assertFalse(True, 'Failed to add Honoured Dead record to week %s, pilot %s%s' % (sw, self.pilot, hdl))

    def test_remove_http_response(self):
        hd = self.first_pw.honour_dead()
        formdata = {'honoured_id' : hd.id} 
        response = self.client.post('/stable/pilots/1/honoured-dead/remove', formdata)

        self.assertEqual(response.status_code, 200, 'HTTP Post request to Add Honoured Dead failed with error (HTTP %s: %s)' \
           % (response.status_code, response.content))

    def test_remove_honoured(self):
        hd = self.first_pw.honour_dead()
        formdata = {'honoured_id' : hd.id} 
        response = self.client.post('/stable/pilots/1/honoured-dead/remove', formdata)

        qs = models.HonouredDead.objects.filter(id=hd.id)
        self.assertEquals(qs.count(), 0, 'Honoured dead should be deleted, instead found %s' % qs)

    def test_list_signatures(self):
        sw = self.stable.get_stableweek(1)

        mech = self.addMech(self.stable, stableweek=sw, mech_name='Wolverine', mech_code='WVR-7D')
        smw = mech.weeks.get(stableweek=sw)

        smw.signature_of = self.pilot
        smw.save()
        
        formdata = {'callsign' : self.pilot.pilot_callsign} 
        response = self.client.get('/stable/pilots/1/honoured-dead/list-signatures', formdata)
        json_data = json.loads(response.content)
        self.assertEquals(len(json_data),1, 'Expected one signature mech to be returned, got %d' % len(json_data))
