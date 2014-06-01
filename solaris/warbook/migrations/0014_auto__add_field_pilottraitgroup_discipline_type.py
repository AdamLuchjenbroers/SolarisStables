# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PilotTraitGroup.discipline_type'
        db.add_column('warbook_pilotdiscipline', 'discipline_type',
                      self.gf('django.db.models.fields.CharField')(default='I', max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PilotTraitGroup.discipline_type'
        db.delete_column('warbook_pilotdiscipline', 'discipline_type')


    models = {
        'warbook.equipment': {
            'Meta': {'ordering': "['equipment_class', 'name']", 'object_name': 'Equipment'},
            'ammo_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.Equipment']", 'null': 'True', 'blank': 'True'}),
            'ammo_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'basic_ammo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '4'}),
            'cost_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'critical_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'critical_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'crittable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'equipment_class': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '1'}),
            'evaluate_last': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_ammo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'FIXME'", 'max_length': '100'}),
            'record_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'splittable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ssw_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'tonnage_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'tonnage_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'weapon_properties': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'warbook.house': {
            'Meta': {'object_name': 'House'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'house': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'house_disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warbook.PilotDiscipline']", 'symmetrical': 'False'}),
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
        'warbook.mechdesignlocation': {
            'Meta': {'unique_together': "(('mech', 'location'),)", 'object_name': 'MechDesignLocation'},
            'armour': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechLocation']"}),
            'mech': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['warbook.MechDesign']"}),
            'structure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'warbook.mechequipment': {
            'Meta': {'object_name': 'MechEquipment'},
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.Equipment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mech': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loadout'", 'to': "orm['warbook.MechDesign']"})
        },
        'warbook.mechlocation': {
            'Meta': {'object_name': 'MechLocation'},
            'criticals': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'rear_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechLocation']", 'null': 'True'})
        },
        'warbook.mounting': {
            'Meta': {'object_name': 'Mounting', 'db_table': "'warbook_mechmounting'"},
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mountings'", 'to': "orm['warbook.MechEquipment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criticals'", 'to': "orm['warbook.MechDesignLocation']"}),
            'rear_firing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slots': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'turret_mounted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'warbook.pilotdiscipline': {
            'Meta': {'object_name': 'PilotDiscipline', '_ormbases': ['warbook.PilotTraitGroup']},
            u'pilottraitgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['warbook.PilotTraitGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'warbook.pilotrank': {
            'Meta': {'object_name': 'PilotRank'},
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

    complete_apps = ['warbook']