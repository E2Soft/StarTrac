# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20, default='')),
                ('color', models.CharField(max_length=8, default='#ffffff')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userextend',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserExtend',
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='tasks.Tag'),
            preserve_default=True,
        ),
    ]
