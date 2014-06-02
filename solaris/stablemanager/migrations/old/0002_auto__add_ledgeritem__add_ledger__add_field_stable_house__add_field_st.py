# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LedgerItem'
        db.create_table('stablemanager_ledgeritem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['stablemanager.Ledger'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('stablemanager', ['LedgerItem'])

        # Adding model 'Ledger'
        db.create_table('stablemanager_ledger', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Stable'])),
            ('week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.BroadcastWeek'])),
            ('opening_balance', self.gf('django.db.models.fields.IntegerField')()),
            ('next_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prev_ledger', null=True, to=orm['stablemanager.Ledger'])),
        ))
        db.send_create_signal('stablemanager', ['Ledger'])

        # Adding field 'Stable.house'
        db.add_column('stablemanager_stable', 'house',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.House'], null=True),
                      keep_default=False)

        # Adding field 'Stable.current_week'
        db.add_column('stablemanager_stable', 'current_week',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.BroadcastWeek'], null=True),
                      keep_default=False)

        # Adding M2M table for field stable_disciplines on 'Stable'
        db.create_table('stablemanager_stable_stable_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stable', models.ForeignKey(orm['stablemanager.stable'], null=False)),
            ('pilotdiscipline', models.ForeignKey(orm['warbook.pilotdiscipline'], null=False))
        ))
        db.create_unique('stablemanager_stable_stable_disciplines', ['stable_id', 'pilotdiscipline_id'])


    def backwards(self, orm):
        # Deleting model 'LedgerItem'
        db.delete_table('stablemanager_ledgeritem')

        # Deleting model 'Ledger'
        db.delete_table('stablemanager_ledger')

        # Deleting field 'Stable.house'
        db.delete_column('stablemanager_stable', 'house_id')

        # Deleting field 'Stable.current_week'
        db.delete_column('stablemanager_stable', 'current_week_id')

        # Removing M2M table for field stable_disciplines on 'Stable'
        db.delete_table('stablemanager_stable_stable_disciplines')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
            'rules': ('django.db.models.fields.TextField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stablemanager.ledger': {
            'Meta': {'object_name': 'Ledger'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prev_ledger'", 'null': 'True', 'to': "orm['stablemanager.Ledger']"}),
            'opening_balance': ('django.db.models.fields.IntegerField', [], {}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']"}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['battlereport.BroadcastWeek']"})
        },
        'stablemanager.ledgeritem': {
            'Meta': {'object_name': 'LedgerItem'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['stablemanager.Ledger']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'stablemanager.mech': {
            'Meta': {'object_name': 'Mech'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']"}),
            'signature_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']", 'null': 'True', 'blank': 'True'}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'null': 'True', 'blank': 'True'})
        },
        'stablemanager.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.House']"}),
            'exp_character_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exp_wounds': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pilot_callsign': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pilot_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pilot_rank': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'skill': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotTrait']", 'symmetrical': 'False', 'through': "orm['stablemanager.PilotTraining']", 'blank': 'True'}),
            'skill_gunnery': ('django.db.models.fields.IntegerField', [], {}),
            'skill_pilotting': ('django.db.models.fields.IntegerField', [], {}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'blank': 'True'})
        },
        'stablemanager.pilottraining': {
            'Meta': {'object_name': 'PilotTraining'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotTrait']"})
        },
        'stablemanager.stable': {
            'Meta': {'object_name': 'Stable'},
            'current_week': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['battlereport.BroadcastWeek']", 'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.House']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {}),
            'stable_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotDiscipline']", 'symmetrical': 'False'}),
            'stable_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'supply_contract': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.Technology']", 'symmetrical': 'False'})
        },
        'warbook.house': {
            'Meta': {'object_name': 'House'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'house': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'house_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotDiscipline']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'warbook.mechdesign': {
            'Meta': {'unique_together': "(('mech_name', 'mech_code'),)", 'object_name': 'MechDesign'},
            'bv_value': ('django.db.models.fields.IntegerField', [], {}),
            'credit_value': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_omni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mech_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mech_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'move_walk': ('django.db.models.fields.IntegerField', [], {}),
            'omni_basechassis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']", 'null': 'True'}),
            'ssw_filename': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'stock_design': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {})
        },
        'warbook.pilotdiscipline': {
            'Meta': {'object_name': 'PilotDiscipline'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'warbook.pilottrait': {
            'Meta': {'object_name': 'PilotTrait', 'db_table': "'warbook_pilotability'"},
            'bv_mod': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotDiscipline']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'trait_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
        },
        'warbook.technology': {
            'Meta': {'object_name': 'Technology'},
            'base_difficulty': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {}),
            'urlname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['stablemanager']