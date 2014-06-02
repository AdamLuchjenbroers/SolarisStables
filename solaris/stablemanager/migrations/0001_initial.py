# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stable'
        db.create_table(u'stablemanager_stable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.House'], null=True)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.BroadcastWeek'], null=True)),
        ))
        db.send_create_signal(u'stablemanager', ['Stable'])

        # Adding M2M table for field supply_contract on 'Stable'
        db.create_table(u'stablemanager_stable_supply_contract', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stable', models.ForeignKey(orm[u'stablemanager.stable'], null=False)),
            ('technology', models.ForeignKey(orm['warbook.technology'], null=False))
        ))
        db.create_unique(u'stablemanager_stable_supply_contract', ['stable_id', 'technology_id'])

        # Adding M2M table for field stable_disciplines on 'Stable'
        db.create_table(u'stablemanager_stable_stable_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stable', models.ForeignKey(orm[u'stablemanager.stable'], null=False)),
            ('pilotdiscipline', models.ForeignKey(orm['warbook.pilotdiscipline'], null=False))
        ))
        db.create_unique(u'stablemanager_stable_stable_disciplines', ['stable_id', 'pilotdiscipline_id'])

        # Adding model 'Pilot'
        db.create_table('stablemanager_pilot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pilots', blank=True, to=orm['stablemanager.Stable'])),
            ('pilot_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('pilot_callsign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.House'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('stablemanager', ['Pilot'])

        # Adding unique constraint on 'Pilot', fields ['stable', 'pilot_callsign']
        db.create_unique('stablemanager_pilot', ['stable_id', 'pilot_callsign'])

        # Adding model 'PilotTraining'
        db.create_table('stablemanager_pilottraining', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pilot_week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.PilotWeek'])),
            ('training', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.PilotTrait'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('stablemanager', ['PilotTraining'])

        # Adding model 'PilotWeek'
        db.create_table('stablemanager_pilotweek', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pilot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weeks', to=orm['stablemanager.Pilot'])),
            ('week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.BroadcastWeek'])),
            ('start_character_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adjust_character_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('assigned_training_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.PilotRank'])),
            ('skill_gunnery', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('skill_piloting', self.gf('django.db.models.fields.IntegerField')(default=6)),
            ('wounds', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('stablemanager', ['PilotWeek'])

        # Adding model 'Mech'
        db.create_table('stablemanager_mech', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Stable'], null=True, blank=True)),
            ('mech_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechDesign'])),
            ('signature_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Pilot'], null=True, blank=True)),
        ))
        db.send_create_signal('stablemanager', ['Mech'])

        # Adding model 'Ledger'
        db.create_table('stablemanager_ledger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ledger', to=orm['stablemanager.Stable'])),
            ('week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['battlereport.BroadcastWeek'])),
            ('opening_balance', self.gf('django.db.models.fields.IntegerField')()),
            ('next_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prev_ledger', null=True, to=orm['stablemanager.Ledger'])),
        ))
        db.send_create_signal('stablemanager', ['Ledger'])

        # Adding unique constraint on 'Ledger', fields ['stable', 'week']
        db.create_unique('stablemanager_ledger', ['stable_id', 'week_id'])

        # Adding model 'LedgerItem'
        db.create_table('stablemanager_ledgeritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['stablemanager.Ledger'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('tied', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stablemanager', ['LedgerItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Ledger', fields ['stable', 'week']
        db.delete_unique('stablemanager_ledger', ['stable_id', 'week_id'])

        # Removing unique constraint on 'Pilot', fields ['stable', 'pilot_callsign']
        db.delete_unique('stablemanager_pilot', ['stable_id', 'pilot_callsign'])

        # Deleting model 'Stable'
        db.delete_table(u'stablemanager_stable')

        # Removing M2M table for field supply_contract on 'Stable'
        db.delete_table('stablemanager_stable_supply_contract')

        # Removing M2M table for field stable_disciplines on 'Stable'
        db.delete_table('stablemanager_stable_stable_disciplines')

        # Deleting model 'Pilot'
        db.delete_table('stablemanager_pilot')

        # Deleting model 'PilotTraining'
        db.delete_table('stablemanager_pilottraining')

        # Deleting model 'PilotWeek'
        db.delete_table('stablemanager_pilotweek')

        # Deleting model 'Mech'
        db.delete_table('stablemanager_mech')

        # Deleting model 'Ledger'
        db.delete_table('stablemanager_ledger')

        # Deleting model 'LedgerItem'
        db.delete_table('stablemanager_ledgeritem')


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
            'skill_gunnery': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'skill_piloting': ('django.db.models.fields.IntegerField', [], {'default': '6'}),
            'start_character_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.BroadcastWeek']"}),
            'wounds': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'stablemanager.stable': {
            'Meta': {'object_name': 'Stable'},
            'current_week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battlereport.BroadcastWeek']", 'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.House']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'auto_train_cp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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