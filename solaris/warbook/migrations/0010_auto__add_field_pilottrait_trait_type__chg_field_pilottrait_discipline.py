# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PilotTrait.trait_type'
        db.add_column('warbook_pilotability', 'trait_type',
                      self.gf('django.db.models.fields.CharField')(default='T', max_length=1),
                      keep_default=False)


        # Changing field 'PilotTrait.discipline'
        db.alter_column('warbook_pilotability', 'discipline_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.PilotDiscipline'], null=True))

    def backwards(self, orm):
        # Deleting field 'PilotTrait.trait_type'
        db.delete_column('warbook_pilotability', 'trait_type')


        # User chose to not deal with backwards NULL issues for 'PilotTrait.discipline'
        raise RuntimeError("Cannot reverse this migration. 'PilotTrait.discipline' and its values cannot be restored.")

    models = {
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
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotDiscipline']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'trait_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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