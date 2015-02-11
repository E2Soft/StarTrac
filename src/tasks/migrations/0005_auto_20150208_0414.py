# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20150118_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='projects',
            new_name='requirement',
        ),
    ]
