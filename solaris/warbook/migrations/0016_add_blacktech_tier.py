# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warbook', '0015_refresh_mechlists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='tier',
            field=models.IntegerField(default=0, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental'), (4, b'Solaris Black-tech')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mechdesign',
            name='tier',
            field=models.IntegerField(default=0, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental'), (4, b'Solaris Black-tech')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='technology',
            name='tier',
            field=models.IntegerField(default=3, choices=[(0, b'Base Technology'), (1, b'Star-League'), (2, b'Advanced'), (3, b'Experimental'), (4, b'Solaris Black-tech')]),
            preserve_default=True,
        ),
    ]
