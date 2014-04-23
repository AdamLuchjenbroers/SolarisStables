# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mech'
        db.create_table('stablemanager_mech', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Stable'], blank=True)),
            ('mech_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechDesign'])),
            ('signature_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Pilot'], blank=True)),
        ))
        db.send_create_signal('stablemanager', ['Mech'])

        # Adding model 'Pilot'
        db.create_table('stablemanager_pilot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Stable'], blank=True)),
            ('pilot_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('pilot_callsign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('skill_gunnery', self.gf('django.db.models.fields.IntegerField')()),
            ('skill_pilotting', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('stablemanager', ['Pilot'])

        # Adding M2M table for field skill on 'Pilot'
        db.create_table('stablemanager_pilot_skill', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pilot', models.ForeignKey(orm['stablemanager.pilot'], null=False)),
            ('pilotability', models.ForeignKey(orm['pilotskill.pilotability'], null=False))
        ))
        db.create_unique('stablemanager_pilot_skill', ['pilot_id', 'pilotability_id'])


    def backwards(self, orm):
        # Deleting model 'Mech'
        db.delete_table('stablemanager_mech')

        # Deleting model 'Pilot'
        db.delete_table('stablemanager_pilot')

        # Removing M2M table for field skill on 'Pilot'
        db.delete_table('stablemanager_pilot_skill')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pilotskill.pilotability': {
            'Meta': {'object_name': 'PilotAbility', 'db_table': "'warbook_pilotability'"},
            'bv_mod': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotDiscipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'stablemanager.mech': {
            'Meta': {'object_name': 'Mech'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']"}),
            'signature_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']", 'blank': 'True'}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'blank': 'True'})
        },
        'stablemanager.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pilot_callsign': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pilot_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pilotskill.PilotAbility']", 'symmetrical': 'False', 'blank': 'True'}),
            'skill_gunnery': ('django.db.models.fields.IntegerField', [], {}),
            'skill_pilotting': ('django.db.models.fields.IntegerField', [], {}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'blank': 'True'})
        },
        'stablemanager.stable': {
            'Meta': {'object_name': 'Stable'},
            'Owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'Reputation': ('django.db.models.fields.IntegerField', [], {}),
            'StableName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'warbook.mechdesign': {
            'Meta': {'unique_together': "(('mech_name', 'mech_code'),)", 'object_name': 'MechDesign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mech_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'move_walk': ('django.db.models.fields.IntegerField', [], {}),
            'stock_design': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warbook.pilotdiscipline': {
            'Meta': {'object_name': 'PilotDiscipline'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['stablemanager']