# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BroadcastWeek.prev_week'
        db.delete_column('battlereport_broadcastweek', 'prev_week_id')

        # Adding field 'BroadcastWeek.next_week'
        db.add_column('battlereport_broadcastweek', 'next_week',
                      self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='prev_week', unique=True, null=True, to=orm['battlereport.BroadcastWeek']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'BroadcastWeek.prev_week'
        db.add_column('battlereport_broadcastweek', 'prev_week',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='next_week', null=True, to=orm['battlereport.BroadcastWeek']),
                      keep_default=False)

        # Deleting field 'BroadcastWeek.next_week'
        db.delete_column('battlereport_broadcastweek', 'next_week_id')


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
            'next': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'prev'", 'unique': 'True', 'to': "orm['battlereport.Zodiac']"}),
            'rules': ('django.db.models.fields.TextField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['battlereport']