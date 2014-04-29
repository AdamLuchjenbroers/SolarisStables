# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TechnologyRollModifier'
        db.create_table('warbook_technologyrollmodifier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('technology', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warbook.Technology'])),
            ('modifier', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('techtree', ['TechnologyRollModifier'])


    def backwards(self, orm):
        # Deleting model 'TechnologyRollModifier'
        db.delete_table('warbook_technologyrollmodifier')


    models = {
        'techtree.technologyrollmodifier': {
            'Meta': {'object_name': 'TechnologyRollModifier', 'db_table': "'warbook_technologyrollmodifier'"},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifier': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warbook.Technology']"})
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

    complete_apps = ['techtree']