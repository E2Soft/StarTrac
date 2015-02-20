# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_userextend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='tasks/static/album'),
            preserve_default=True,
        ),
    ]
