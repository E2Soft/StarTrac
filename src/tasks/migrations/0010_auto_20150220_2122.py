# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_commit_committer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEvent',
            fields=[
                ('event_ptr', models.OneToOneField(to='tasks.Event', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='PriorityChange',
            fields=[
                ('event_ptr', models.OneToOneField(to='tasks.Event', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('new_priority', models.CharField(default='L', max_length=1, choices=[('C', 'Critical'), ('H', 'High'), ('M', 'Medium'), ('L', 'Low')])),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='ResolveEvent',
            fields=[
                ('event_ptr', models.OneToOneField(to='tasks.Event', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('new_resolve', models.CharField(default='O', max_length=1, choices=[('N', 'Open'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('R', 'Worksforme')])),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_kind',
            field=models.CharField(default='C', max_length=1, choices=[('K', 'Comment'), ('C', 'Commit'), ('S', 'StateChange'), ('P', 'PriorityChange'), ('R', 'Resolve'), ('A', 'Adding')]),
            preserve_default=True,
        ),
    ]
