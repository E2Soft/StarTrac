# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20150211_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='commit_url',
        ),
        migrations.AddField(
            model_name='commit',
            name='committed_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 11, 22, 34, 55, 65659, tzinfo=utc), verbose_name='date committed'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commit',
            name='hex_sha',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commit',
            name='message',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
