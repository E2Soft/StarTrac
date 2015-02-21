# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEvent',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, to='tasks.Event', parent_link=True, primary_key=True)),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, to='tasks.Event', parent_link=True, primary_key=True)),
                ('hex_sha', models.CharField(max_length=40)),
                ('message', models.CharField(max_length=300)),
                ('committer_name', models.CharField(max_length=70, blank=True, null=True)),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='PriorityChange',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, to='tasks.Event', parent_link=True, primary_key=True)),
                ('new_priority', models.CharField(max_length=1, choices=[('C', 'Critical'), ('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='L')),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='ResolveEvent',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, to='tasks.Event', parent_link=True, primary_key=True)),
                ('new_resolve', models.CharField(max_length=1, choices=[('N', 'Open'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')], default='O')),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, default='')),
                ('color', models.CharField(max_length=8, default='#000000')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtend',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('picture', models.ImageField(upload_to='album', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='commit',
            name='committer_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='milestone',
            old_name='summry',
            new_name='summary',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='projects',
            new_name='requirement',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='milestone',
            field=models.ForeignKey(blank=True, null=True, to='tasks.Milestone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='resolve_type',
            field=models.CharField(max_length=1, choices=[('N', 'Open'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')], default='N'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='tasks.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_kind',
            field=models.CharField(max_length=1, choices=[('K', 'Comment'), ('C', 'Commit'), ('S', 'StateChange'), ('P', 'PriorityChange'), ('R', 'Resolve'), ('A', 'Adding')], default='C'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='requirement_task',
            field=models.ForeignKey(blank=True, null=True, to='tasks.RequirementTask'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
