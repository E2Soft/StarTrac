# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('tasks', '0011_auto_20150221_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtend',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('picture', models.ImageField(null=True, blank=True, upload_to='album')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#000000', max_length=8),
            preserve_default=True,
        ),
    ]
