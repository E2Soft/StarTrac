# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userextend',
            options={'verbose_name_plural': 'users', 'verbose_name': 'user'},
        ),
        migrations.RemoveField(
            model_name='userextend',
            name='id',
        ),
        migrations.AlterField(
            model_name='userextend',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='album'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userextend',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
