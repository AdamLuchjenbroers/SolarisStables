# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrainingCost'
        db.create_table('warbook_trainingcost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('training', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('train_from', self.gf('django.db.models.fields.IntegerField')()),
            ('train_to', self.gf('django.db.models.fields.IntegerField')()),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('warbook', ['TrainingCost'])

        # Adding unique constraint on 'TrainingCost', fields ['training', 'train_to']
        db.create_unique('warbook_trainingcost', ['training', 'train_to'])

        # Adding model 'PilotRank'
        db.create_table('warbook_pilotrank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('min_gunnery', self.gf('django.db.models.fields.IntegerField')()),
            ('min_piloting', self.gf('django.db.models.fields.IntegerField')()),
            ('skills_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('auto_train_cp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('promotion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.PilotRank'], null=True, blank=True)),
        ))
        db.send_create_signal('warbook', ['PilotRank'])

        # Adding model 'PilotTraitGroup'
        db.create_table('warbook_pilotdiscipline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('discipline_type', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
        ))
        db.send_create_signal('warbook', ['PilotTraitGroup'])

        # Adding model 'PilotTrait'
        db.create_table('warbook_pilotability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='traits', null=True, to=orm['warbook.PilotTraitGroup'])),
            ('bv_mod', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3)),
        ))
        db.send_create_signal('warbook', ['PilotTrait'])

        # Adding model 'House'
        db.create_table('warbook_house', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('warbook', ['House'])

        # Adding M2M table for field house_disciplines on 'House'
        m2m_table_name = db.shorten_name('warbook_house_house_disciplines')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('house', models.ForeignKey(orm['warbook.house'], null=False)),
            ('pilotdiscipline', models.ForeignKey(orm['warbook.pilotdiscipline'], null=False))
        ))
        db.create_unique(m2m_table_name, ['house_id', 'pilotdiscipline_id'])

        # Adding model 'Technology'
        db.create_table('warbook_technology', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mech_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('omni_loadout', self.gf('django.db.models.fields.CharField')(default='Base', max_length=30, blank=True)),
            ('stock_design', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('credit_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('bv_value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tonnage', self.gf('django.db.models.fields.IntegerField')()),
            ('engine_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('is_omni', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ssw_filename', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('motive_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('tech_base', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('production_type', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('omni_basechassis', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='loadouts', null=True, to=orm['warbook.MechDesign'])),
        ))
        db.send_create_signal('warbook', ['MechDesign'])

        # Adding unique constraint on 'MechDesign', fields ['mech_name', 'mech_code', 'omni_loadout']
        db.create_unique('warbook_mechdesign', ['mech_name', 'mech_code', 'omni_loadout'])

        # Adding unique constraint on 'MechDesign', fields ['ssw_filename', 'omni_loadout']
        db.create_unique('warbook_mechdesign', ['ssw_filename', 'omni_loadout'])

        # Adding model 'MechLocation'
        db.create_table('warbook_mechlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('criticals', self.gf('django.db.models.fields.IntegerField')()),
            ('rear_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechLocation'], null=True)),
        ))
        db.send_create_signal('warbook', ['MechLocation'])

        # Adding model 'MechDesignLocation'
        db.create_table('warbook_mechdesignlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', to=orm['warbook.MechDesign'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.MechLocation'])),
            ('armour', self.gf('django.db.models.fields.IntegerField')()),
            ('structure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('warbook', ['MechDesignLocation'])

        # Adding unique constraint on 'MechDesignLocation', fields ['mech', 'location']
        db.create_unique('warbook_mechdesignlocation', ['mech_id', 'location_id'])

        # Adding model 'Equipment'
        db.create_table('warbook_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='FIXME', max_length=100)),
            ('ssw_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('tonnage_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('tonnage_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('critical_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('critical_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('cost_func', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('cost_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=4)),
            ('splittable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('crittable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_ammo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('basic_ammo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ammo_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.Equipment'], null=True, blank=True)),
            ('ammo_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weapon_properties', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('evaluate_last', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('record_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('equipment_class', self.gf('django.db.models.fields.CharField')(default='?', max_length=1)),
        ))
        db.send_create_signal('warbook', ['Equipment'])

        # Adding model 'MechEquipment'
        db.create_table('warbook_mechequipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mech', self.gf('django.db.models.fields.related.ForeignKey')(related_name='loadout', to=orm['warbook.MechDesign'])),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.Equipment'])),
        ))
        db.send_create_signal('warbook', ['MechEquipment'])

        # Adding model 'Mounting'
        db.create_table('warbook_mechmounting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criticals', to=orm['warbook.MechDesignLocation'])),
            ('equipment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mountings', to=orm['warbook.MechEquipment'])),
            ('slots', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('rear_firing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('turret_mounted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('warbook', ['Mounting'])


    def backwards(self, orm):
        # Removing unique constraint on 'MechDesignLocation', fields ['mech', 'location']
        db.delete_unique('warbook_mechdesignlocation', ['mech_id', 'location_id'])

        # Removing unique constraint on 'MechDesign', fields ['ssw_filename', 'omni_loadout']
        db.delete_unique('warbook_mechdesign', ['ssw_filename', 'omni_loadout'])

        # Removing unique constraint on 'MechDesign', fields ['mech_name', 'mech_code', 'omni_loadout']
        db.delete_unique('warbook_mechdesign', ['mech_name', 'mech_code', 'omni_loadout'])

        # Removing unique constraint on 'TrainingCost', fields ['training', 'train_to']
        db.delete_unique('warbook_trainingcost', ['training', 'train_to'])

        # Deleting model 'TrainingCost'
        db.delete_table('warbook_trainingcost')

        # Deleting model 'PilotRank'
        db.delete_table('warbook_pilotrank')

        # Deleting model 'PilotTraitGroup'
        db.delete_table('warbook_pilotdiscipline')

        # Deleting model 'PilotTrait'
        db.delete_table('warbook_pilotability')

        # Deleting model 'House'
        db.delete_table('warbook_house')

        # Removing M2M table for field house_disciplines on 'House'
        db.delete_table(db.shorten_name('warbook_house_house_disciplines'))

        # Deleting model 'Technology'
        db.delete_table('warbook_technology')

        # Deleting model 'MechDesign'
        db.delete_table('warbook_mechdesign')

        # Deleting model 'MechLocation'
        db.delete_table('warbook_mechlocation')

        # Deleting model 'MechDesignLocation'
        db.delete_table('warbook_mechdesignlocation')

        # Deleting model 'Equipment'
        db.delete_table('warbook_equipment')

        # Deleting model 'MechEquipment'
        db.delete_table('warbook_mechequipment')

        # Deleting model 'Mounting'
        db.delete_table('warbook_mechmounting')


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
            'omni_basechassis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loadouts'", 'null': 'True', 'to': "orm['warbook.MechDesign']"}),
            'omni_loadout': ('django.db.models.fields.CharField', [], {'default': "'Base'", 'max_length': '30', 'blank': 'True'}),
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
        },
        'warbook.trainingcost': {
            'Meta': {'unique_together': "(('training', 'train_to'),)", 'object_name': 'TrainingCost'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'train_from': ('django.db.models.fields.IntegerField', [], {}),
            'train_to': ('django.db.models.fields.IntegerField', [], {}),
            'training': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    # Load JSON Initial Data
    call_command('loaddata', 'data/warbook.house.json')
    call_command('loaddata', 'data/warbook.mechlocation.json')
    call_command('loaddata', 'data/warbook.technology.json')
    call_command('loaddata', 'data/warbook.technologyrollmodifier.json')
    call_command('loaddata', 'data/warbook.trainingcost.json')
    call_command('loaddata', 'data/warbook.pilotdiscipline.json')
    call_command('loaddata', 'data/warbook.pilotskill.json')
    complete_apps = ['warbook']
