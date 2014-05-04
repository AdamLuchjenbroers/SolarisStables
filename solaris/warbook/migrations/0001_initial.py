# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PilotDiscipline'
        db.create_table('warbook_pilotdiscipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('warbook', ['PilotDiscipline'])

        # Adding model 'PilotTrait'
        db.create_table('warbook_pilotability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.PilotDiscipline'], null=True, blank=True)),
            ('bv_mod', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3)),
            ('trait_type', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
        ))
        db.send_create_signal('warbook', ['PilotTrait'])

        # Adding model 'House'
        db.create_table('warbook_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('warbook', ['House'])

        # Adding M2M table for field house_disciplines on 'House'
        db.create_table('warbook_house_house_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('house', models.ForeignKey(orm['warbook.house'], null=False)),
            ('pilotdiscipline', models.ForeignKey(orm['warbook.pilotdiscipline'], null=False))
        ))
        db.create_unique('warbook_house_house_disciplines', ['house_id', 'pilotdiscipline_id'])

        # Adding model 'Technology'
        db.create_table('warbook_technology', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('urlname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('base_difficulty', self.gf('django.db.models.fields.IntegerField')()),
            ('tier', self.gf('django.db.models.fields.IntegerField')()),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('warbook', ['Technology'])

        # Adding model 'MechDesign'
        db.create_table('warbook_mechdesign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mech_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mech_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('omni_loadout', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=30)),
            ('stock_design', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('credit_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('bv_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tonnage', self.gf('django.db.models.fields.IntegerField')()),
            ('engine_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('is_omni', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('omni_basechassis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechDesign'], null=True)),
            ('ssw_filename', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('warbook', ['MechDesign'])

        # Adding unique constraint on 'MechDesign', fields ['mech_name', 'mech_code', 'omni_loadout']
        db.create_unique('warbook_mechdesign', ['mech_name', 'mech_code', 'omni_loadout'])

        # Adding unique constraint on 'MechDesign', fields ['ssw_filename', 'omni_loadout']
        db.create_unique('warbook_mechdesign', ['ssw_filename', 'omni_loadout'])

        # Adding model 'MechLocation'
        db.create_table('warbook_mechlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('criticals', self.gf('django.db.models.fields.IntegerField')()),
            ('rear_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechLocation'], null=True)),
        ))
        db.send_create_signal('warbook', ['MechLocation'])

        # Adding model 'MechDesignLocation'
        db.create_table('warbook_mechdesignlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', to=orm['warbook.MechDesign'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechLocation'])),
            ('armor', self.gf('django.db.models.fields.IntegerField')()),
            ('structure', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('warbook', ['MechDesignLocation'])

        # Adding unique constraint on 'MechDesignLocation', fields ['mech', 'location']
        db.create_unique('warbook_mechdesignlocation', ['mech_id', 'location_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MechDesignLocation', fields ['mech', 'location']
        db.delete_unique('warbook_mechdesignlocation', ['mech_id', 'location_id'])

        # Removing unique constraint on 'MechDesign', fields ['ssw_filename', 'omni_loadout']
        db.delete_unique('warbook_mechdesign', ['ssw_filename', 'omni_loadout'])

        # Removing unique constraint on 'MechDesign', fields ['mech_name', 'mech_code', 'omni_loadout']
        db.delete_unique('warbook_mechdesign', ['mech_name', 'mech_code', 'omni_loadout'])

        # Deleting model 'PilotDiscipline'
        db.delete_table('warbook_pilotdiscipline')

        # Deleting model 'PilotTrait'
        db.delete_table('warbook_pilotability')

        # Deleting model 'House'
        db.delete_table('warbook_house')

        # Removing M2M table for field house_disciplines on 'House'
        db.delete_table('warbook_house_house_disciplines')

        # Deleting model 'Technology'
        db.delete_table('warbook_technology')

        # Deleting model 'MechDesign'
        db.delete_table('warbook_mechdesign')

        # Deleting model 'MechLocation'
        db.delete_table('warbook_mechlocation')

        # Deleting model 'MechDesignLocation'
        db.delete_table('warbook_mechdesignlocation')


    models = {
        'warbook.house': {
            'Meta': {'object_name': 'House'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'house': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'house_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotDiscipline']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'warbook.mechdesign': {
            'Meta': {'unique_together': "(('mech_name', 'mech_code', 'omni_loadout'), ('ssw_filename', 'omni_loadout'))", 'object_name': 'MechDesign'},
            'bv_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'credit_value': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'engine_rating': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_omni': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mech_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mech_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'mech_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'omni_basechassis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']", 'null': 'True'}),
            'omni_loadout': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '30'}),
            'ssw_filename': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'stock_design': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tonnage': ('django.db.models.fields.IntegerField', [], {})
        },
        'warbook.mechdesignlocation': {
            'Meta': {'unique_together': "(('mech', 'location'),)", 'object_name': 'MechDesignLocation'},
            'armor': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechLocation']"}),
            'mech': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['warbook.MechDesign']"}),
            'structure': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'warbook.mechlocation': {
            'Meta': {'object_name': 'MechLocation'},
            'criticals': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'rear_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechLocation']", 'null': 'True'})
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

    complete_apps = ['warbook']