# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from django.core.management import call_command
from solaris.battlereport.models import BroadcastWeek, Zodiac

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zodiac'
        db.create_table('battlereport_zodiac', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rules', self.gf('django.db.models.fields.TextField')()),
            ('next', self.gf('django.db.models.fields.related.OneToOneField')(related_name='prev', unique=True, null=True, to=orm['battlereport.Zodiac'])),
        ))
        db.send_create_signal('battlereport', ['Zodiac'])
        call_command('loaddata','data/battlereport.zodiac.json')
        
        # Adding model 'BroadcastWeek'
        db.create_table('battlereport_broadcastweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week_number', self.gf('django.db.models.fields.IntegerField')()),
            ('sign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.Zodiac'])),
            ('next_week', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='prev_week', unique=True, null=True, to=orm['battlereport.BroadcastWeek'])),
        ))
        db.send_create_signal('battlereport', ['BroadcastWeek'])

        # Create Week 1
        week_one = BroadcastWeek(
            week_number = 1
        ,   sign = Zodiac.objects.get(sign='Pig')
        )
        week_one.save()

    def backwards(self, orm):
        # Deleting model 'Zodiac'
        db.delete_table('battlereport_zodiac')

        # Deleting model 'BroadcastWeek'
        db.delete_table('battlereport_broadcastweek')


    models = {
        'battlereport.broadcastweek': {
            'Meta': {'object_name': 'BroadcastWeek'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_week': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'prev_week'", 'unique': 'True', 'null': 'True', 'to': "orm['battlereport.BroadcastWeek']"}),
            'sign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['battlereport.Zodiac']"}),
            'week_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'battlereport.zodiac': {
            'Meta': {'object_name': 'Zodiac'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'prev'", 'unique': 'True', 'null': 'True', 'to': "orm['battlereport.Zodiac']"}),
            'rules': ('django.db.models.fields.TextField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['battlereport']
