# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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

        # Adding model 'PilotDiscipline'
        db.create_table('warbook_pilotdiscipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
            ('urlname', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('warbook', ['PilotDiscipline'])

        # Adding model 'MechDesign'
        db.create_table('warbook_mechdesign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('mech_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('stock_design', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('tonnage', self.gf('django.db.models.fields.IntegerField')()),
            ('move_walk', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('warbook', ['MechDesign'])

        # Adding unique constraint on 'MechDesign', fields ['mech_name', 'mech_code']
        db.create_unique('warbook_mechdesign', ['mech_name', 'mech_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'MechDesign', fields ['mech_name', 'mech_code']
        db.delete_unique('warbook_mechdesign', ['mech_name', 'mech_code'])

        # Deleting model 'Technology'
        db.delete_table('warbook_technology')

        # Deleting model 'PilotDiscipline'
        db.delete_table('warbook_pilotdiscipline')

        # Deleting model 'MechDesign'
        db.delete_table('warbook_mechdesign')


    models = {
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
            'urlname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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