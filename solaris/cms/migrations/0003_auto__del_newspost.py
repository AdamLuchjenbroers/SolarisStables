# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NewsPost'
        db.delete_table(u'cms_newspost')


    def backwards(self, orm):
        # Adding model 'NewsPost'
        db.create_table(u'cms_newspost', (
            ('post_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('_content_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('poster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('content', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cms', ['NewsPost'])


    models = {
        u'cms.staticcontent': {
            'Meta': {'object_name': 'StaticContent'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'toplevel': ('django.db.models.fields.BooleanField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['cms']