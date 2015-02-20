# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20150208_0414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='milestone',
            old_name='summry',
            new_name='summary',
        ),
        migrations.AlterField(
            model_name='requirementtask',
            name='resolve_type',
            field=models.CharField(choices=[('N', 'Open'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')], default='N', max_length=1),
            preserve_default=True,
        ),
    ]
