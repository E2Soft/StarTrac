# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20141231_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementtask',
            name='resolve_type',
            field=models.CharField(max_length=1, default='N', choices=[('N', 'None'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requirementtask',
            name='state_kind',
            field=models.CharField(max_length=1, default='C', choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')]),
            preserve_default=True,
        ),
    ]
