# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('content', markitup.fields.MarkupField(no_rendered_field=True)),
                ('post_date', models.DateField(auto_now_add=True)),
                ('_content_rendered', models.TextField(editable=False, blank=True)),
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News Post',
                'verbose_name_plural': 'News Posts',
                'permissions': (('post_news', 'Post News Items'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaticContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('toplevel', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Static Content',
                'verbose_name_plural': 'Static Content',
            },
            bases=(models.Model,),
        ),
    ]
