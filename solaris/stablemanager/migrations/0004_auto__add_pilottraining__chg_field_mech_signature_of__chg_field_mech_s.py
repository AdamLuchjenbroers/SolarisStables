# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PilotTraining'
        db.create_table('stablemanager_pilottraining', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pilot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Pilot'])),
            ('training', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pilotskill.PilotAbility'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('stablemanager', ['PilotTraining'])


        # Changing field 'Mech.signature_of' (Change already in production
        #db.alter_column('stablemanager_mech', 'signature_of_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Pilot'], null=True))

        # Changing field 'Mech.stable'
        #db.alter_column('stablemanager_mech', 'stable_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stablemanager.Stable'], null=True))
        # Removing M2M table for field skill on 'Pilot'
        db.delete_table('stablemanager_pilot_skill')

        # Deleting field 'Stable.Owner'
        db.delete_column('stablemanager_stable', 'Owner_id')

        # Adding field 'Stable.owner'
        db.add_column('stablemanager_stable', 'owner',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PilotTraining'
        db.delete_table('stablemanager_pilottraining')


        # User chose to not deal with backwards NULL issues for 'Mech.signature_of'
        raise RuntimeError("Cannot reverse this migration. 'Mech.signature_of' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Mech.stable'
        raise RuntimeError("Cannot reverse this migration. 'Mech.stable' and its values cannot be restored.")
        # Adding M2M table for field skill on 'Pilot'
        db.create_table('stablemanager_pilot_skill', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pilot', models.ForeignKey(orm['stablemanager.pilot'], null=False)),
            ('pilotability', models.ForeignKey(orm['pilotskill.pilotability'], null=False))
        ))
        db.create_unique('stablemanager_pilot_skill', ['pilot_id', 'pilotability_id'])


        # User chose to not deal with backwards NULL issues for 'Stable.Owner'
        raise RuntimeError("Cannot reverse this migration. 'Stable.Owner' and its values cannot be restored.")
        # Deleting field 'Stable.owner'
        db.delete_column('stablemanager_stable', 'owner_id')


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
            'signature_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']", 'null': 'True', 'blank': 'True'}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'null': 'True', 'blank': 'True'})
        },
        'stablemanager.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pilot_callsign': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pilot_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pilotskill.PilotAbility']", 'symmetrical': 'False', 'through': "orm['stablemanager.PilotTraining']", 'blank': 'True'}),
            'skill_gunnery': ('django.db.models.fields.IntegerField', [], {}),
            'skill_pilotting': ('django.db.models.fields.IntegerField', [], {}),
            'stable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Stable']", 'blank': 'True'})
        },
        'stablemanager.pilottraining': {
            'Meta': {'object_name': 'PilotTraining'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stablemanager.Pilot']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pilotskill.PilotAbility']"})
        },
        'stablemanager.stable': {
            'Meta': {'object_name': 'Stable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {}),
            'stable_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'supply_contract': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.Technology']", 'symmetrical': 'False'})
        },
        'warbook.mechdesign': {
            'Meta': {'unique_together': "(('mech_name', 'mech_code'),)", 'object_name': 'MechDesign'},
            'bv_value': ('django.db.models.fields.IntegerField', [], {}),
            'credit_value': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mech_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'move_walk': ('django.db.models.fields.IntegerField', [], {}),
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