# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20141229_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementtask',
            name='resolve_type',
            field=models.CharField(max_length=1, default='F', choices=[('N', 'None'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')]),
            preserve_default=True,
        ),
    ]
