# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Zodiac.next'
        db.alter_column('battlereport_zodiac', 'next_id', self.gf('django.db.models.fields.related.OneToOneField')(default=-1, unique=True, to=orm['battlereport.Zodiac']))

    def backwards(self, orm):

        # Changing field 'Zodiac.next'
        db.alter_column('battlereport_zodiac', 'next_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['battlereport.Zodiac']))

    models = {
        'battlereport.broadcastweek': {
            'Meta': {'object_name': 'BroadcastWeek'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev_week': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'next_week'", 'null': 'True', 'to': "orm['battlereport.BroadcastWeek']"}),
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