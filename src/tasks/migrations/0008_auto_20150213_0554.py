# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20150211_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='committed_date',
        ),
        migrations.AddField(
            model_name='commit',
            name='committer_name',
            field=models.CharField(max_length=70, blank=True, null=True),
            preserve_default=True,
        ),
    ]
