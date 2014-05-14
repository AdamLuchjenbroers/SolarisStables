# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mounting'
        db.create_table('warbook_mechmounting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criticals', to=orm['warbook.MechDesignLocation'])),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mountings', to=orm['warbook.MechEquipment'])),
            ('slots', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('warbook', ['Mounting'])

        # Adding model 'MechEquipment'
        db.create_table('warbook_mechequipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech', self.gf('django.db.models.fields.related.ForeignKey')(related_name='loadout', to=orm['warbook.MechDesign'])),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.Equipment'])),
        ))
        db.send_create_signal('warbook', ['MechEquipment'])

        # Adding model 'Equipment'
        db.create_table('warbook_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ssw_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('tonnage_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('tonnage_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1)),
            ('critical_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('critical_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1)),
            ('cost_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('cost_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=1)),
            ('splittable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('crittable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_ammo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ammo_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.Equipment'], null=True, blank=True)),
            ('ammo_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weapon_properties', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('equipment_class', self.gf('django.db.models.fields.CharField')(default='?', max_length=1)),
        ))
        db.send_create_signal('warbook', ['Equipment'])

        # Deleting field 'MechDesignLocation.armor'
        db.delete_column(u'warbook_mechdesignlocation', 'armor')

        # Adding field 'MechDesignLocation.armour'
        db.add_column('warbook_mechdesignlocation', 'armour',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Mounting'
        db.delete_table('warbook_mechmounting')

        # Deleting model 'MechEquipment'
        db.delete_table('warbook_mechequipment')

        # Deleting model 'Equipment'
        db.delete_table('warbook_equipment')

        # Adding field 'MechDesignLocation.armor'
        db.add_column(u'warbook_mechdesignlocation', 'armor',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'MechDesignLocation.armour'
        db.delete_column('warbook_mechdesignlocation', 'armour')


    models = {
        'warbook.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'ammo_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.Equipment']", 'null': 'True', 'blank': 'True'}),
            'ammo_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cost_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '1'}),
            'cost_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'critical_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1'}),
            'critical_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'crittable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'equipment_class': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '1'}),
            'has_ammo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'splittable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ssw_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'tonnage_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1'}),
            'tonnage_func': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'weapon_properties': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
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
            'omni_basechassis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.MechDesign']", 'null': 'True', 'blank': 'True'}),
            'omni_loadout': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '30', 'blank': 'True'}),
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
            'structure': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
            'slots': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'warbook.pilotdiscipline': {
            'Meta': {'object_name': 'PilotDiscipline'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'warbook.pilottrait': {
            'Meta': {'object_name': 'PilotTrait', 'db_table': "'warbook_pilotability'"},
            'bv_mod': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.PilotDiscipline']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'trait_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
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