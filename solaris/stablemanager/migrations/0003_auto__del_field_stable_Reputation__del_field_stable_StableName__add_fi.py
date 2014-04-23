# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Stable.Reputation'
        db.delete_column('stablemanager_stable', 'Reputation')

        # Deleting field 'Stable.StableName'
        db.delete_column('stablemanager_stable', 'StableName')

        # Adding field 'Stable.stable_name'
        db.add_column('stablemanager_stable', 'stable_name',
                      self.gf('django.db.models.fields.CharField')(default='Fixme', max_length=200),
                      keep_default=False)

        # Adding field 'Stable.reputation'
        db.add_column('stablemanager_stable', 'reputation',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field supply_contract on 'Stable'
        db.create_table('stablemanager_stable_supply_contract', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stable', models.ForeignKey(orm['stablemanager.stable'], null=False)),
            ('technology', models.ForeignKey(orm['warbook.technology'], null=False))
        ))
        db.create_unique('stablemanager_stable_supply_contract', ['stable_id', 'technology_id'])


    def backwards(self, orm):
        # Adding field 'Stable.Reputation'
        db.add_column('stablemanager_stable', 'Reputation',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stable.StableName'
        db.add_column('stablemanager_stable', 'StableName',
                      self.gf('django.db.models.fields.CharField')(default='Fixme', max_length=200),
                      keep_default=False)

        # Deleting field 'Stable.stable_name'
        db.delete_column('stablemanager_stable', 'stable_name')

        # Deleting field 'Stable.reputation'
        db.delete_column('stablemanager_stable', 'reputation')

        # Removing M2M table for field supply_contract on 'Stable'
        db.delete_table('stablemanager_stable_supply_contract')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {}),
            'stable_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'supply_contract': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.Technology']", 'symmetrical': 'False'})
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