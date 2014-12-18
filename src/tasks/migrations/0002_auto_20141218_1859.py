# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='event',
            field=models.ForeignKey(to='tasks.Event', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requirementtask',
            name='project_tast_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='milestone',
            field=models.ForeignKey(to='tasks.Milestone', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='projects',
            field=models.ForeignKey(to='tasks.Requirement', null=True),
            preserve_default=True,
        ),
    ]
