# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, to='tasks.Event', parent_link=True, primary_key=True, serialize=False)),
                ('commit_url', models.URLField()),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='milestone',
            field=models.ForeignKey(blank=True, to='tasks.Milestone', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='resolve_type',
            field=models.CharField(default='F', choices=[('F', 'None'), ('F', 'Fixed'), ('I', 'Invalid'), ('W', 'Wontfix'), ('D', 'Duplicate'), ('D', 'Worksforme')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_kind',
            field=models.CharField(default='C', choices=[('K', 'Comment'), ('C', 'Commit'), ('S', 'StateChange')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='requirement_task',
            field=models.ForeignKey(blank=True, to='tasks.RequirementTask', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requirementtask',
            name='state_kind',
            field=models.CharField(default='K', choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
