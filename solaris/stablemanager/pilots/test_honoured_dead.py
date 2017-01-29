
from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

from solaris.stablemanager.tests import StableTestMixin

from . import models

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
        first_sw = self.stable.get_stableweek()
        second_sw = first_sw.advance()

        hd = self.get_first_pw().honour_dead()
        self.assertEquals(hd.next_week.prev_week, hd, 'o.O - WTF?')
        hd.next_week.delete()

        # Re-fetch from Database due to ORM de-sync issues
        # TODO: Clean this up after migrating to Django 1.8+
        hd = models.HonouredDead.objects.get(id=hd.id)
        self.assertFalse(hd.removed, 'Previous week not marked as removed')      
       

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

        self.client.post('/stable/pilots/1/honoured-dead/remove', formdata)

        qs = models.HonouredDead.objects.filter(id=hd.id)
        self.assertNotEquals(qs.count, 0, 'Honoured dead should be deleted, instead found: ' % qs)

    def test_list_signatures(self):
        sw = self.stable.get_stableweek(1)

        mech = self.addMech(mech_name='Wolverine', mech_code='WVR-7D')
        smw = mech.weeks.get(week=sw)

        smw.signature_of = self.pilot
        smw.save()
        
        formdata = {'callsign' : self.pilot.pilot_callsign} 
        response = self.client.get('/stable/pilots/1/honoured-dead/list-signatures', formdata)
        json_data = json.loads(response)
        self.assertEquals(json_data.length,1, 'Expected one signature mech to be returned, got %d' % json_data.length)
