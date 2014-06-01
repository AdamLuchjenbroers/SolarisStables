# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Pilot', fields ['pilot_callsign', 'stable']
        db.create_unique('stablemanager_pilot', ['pilot_callsign', 'stable_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Pilot', fields ['pilot_callsign', 'stable']
        db.delete_unique('stablemanager_pilot', ['pilot_callsign', 'stable_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'battlereport.broadcastweek': {
            'Meta': {'object_name': 'BroadcastWeek'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_week': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'prev_week'", 'unique': 'True', 'null': 'True', 'to': u"orm['battlereport.BroadcastWeek']"}),
            'sign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.Zodiac']"}),
            'week_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'battlereport.zodiac': {
            'Meta': {'object_name': 'Zodiac'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'prev'", 'unique': 'True', 'null': 'True', 'to': u"orm['battlereport.Zodiac']"}),
            'rules': ('django.db.models.fields.TextField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stablemanager.ledger': {
            'Meta': {'unique_together': "(('stable', 'week'),)", 'object_name': 'Ledger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prev_ledger'", 'null': 'True', 'to': "orm['stablemanager.Ledger']"}),
            'opening_balance': ('django.db.models.fields.IntegerField', [], {}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ledger'", 'to': u"orm['stablemanager.Stable']"}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.BroadcastWeek']"})
        },
        'stablemanager.ledgeritem': {
            'Meta': {'object_name': 'LedgerItem'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['stablemanager.Ledger']"}),
            'tied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'stablemanager.mech': {
            'Meta': {'object_name': 'Mech'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']"}),
            'signature_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']", 'null': 'True', 'blank': 'True'}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stablemanager.Stable']", 'null': 'True', 'blank': 'True'})
        },
        'stablemanager.pilot': {
            'Meta': {'unique_together': "(('stable', 'pilot_callsign'),)", 'object_name': 'Pilot'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.House']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pilot_callsign': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pilot_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pilots'", 'blank': 'True', 'to': u"orm['stablemanager.Stable']"})
        },
        'stablemanager.pilottraining': {
            'Meta': {'object_name': 'PilotTraining'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pilot_week': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.PilotWeek']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotTrait']"})
        },
        'stablemanager.pilotweek': {
            'Meta': {'object_name': 'PilotWeek'},
            'adjust_character_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'assigned_training_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weeks'", 'to': "orm['stablemanager.Pilot']"}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotRank']"}),
            'skill': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['warbook.PilotTrait']", 'null': 'True', 'through': "orm['stablemanager.PilotTraining']", 'blank': 'True'}),
            'skill_gunnery': ('django.db.models.fields.IntegerField', [], {}),
            'skill_pilotting': ('django.db.models.fields.IntegerField', [], {}),
            'start_character_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.BroadcastWeek']"}),
            'wounds': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stablemanager.stable': {
            'Meta': {'object_name': 'Stable'},
            'current_week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.BroadcastWeek']", 'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.House']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {}),
            'stable_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotTraitGroup']", 'symmetrical': 'False'}),
            'stable_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'supply_contract': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.Technology']", 'symmetrical': 'False'})
        },
        'warbook.house': {
            'Meta': {'object_name': 'House'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'house': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'house_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotTraitGroup']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'warbook.mechdesign': {
            'Meta': {'ordering': "['tonnage', 'mech_name', 'mech_code', 'omni_loadout']", 'unique_together': "(('mech_name', 'mech_code', 'omni_loadout'), ('ssw_filename', 'omni_loadout'))", 'object_name': 'MechDesign'},
            'bv_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'credit_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'engine_rating': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_omni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mech_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mech_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'motive_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'omni_basechassis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']", 'null': 'True', 'blank': 'True'}),
            'omni_loadout': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '30', 'blank': 'True'}),
            'production_type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'ssw_filename': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'stock_design': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tech_base': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {})
        },
        'warbook.pilotrank': {
            'Meta': {'object_name': 'PilotRank'},
            'auto_train_cp': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_gunnery': ('django.db.models.fields.IntegerField', [], {}),
            'min_piloting': ('django.db.models.fields.IntegerField', [], {}),
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotRank']", 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'skills_limit': ('django.db.models.fields.IntegerField', [], {})
        },
        'warbook.pilottrait': {
            'Meta': {'object_name': 'PilotTrait', 'db_table': "'warbook_pilotability'"},
            'bv_mod': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'traits'", 'null': 'True', 'to': "orm['warbook.PilotTraitGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'warbook.pilottraitgroup': {
            'Meta': {'object_name': 'PilotTraitGroup', 'db_table': "'warbook_pilotdiscipline'"},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'discipline_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'warbook.technology': {
            'Meta': {'object_name': 'Technology'},
            'base_difficulty': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {}),
            'urlname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['stablemanager']