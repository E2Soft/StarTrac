# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('event_kind', models.CharField(max_length=1, choices=[('C', 'Accepted'), ('P', 'Created')], default='C')),
                ('date_created', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='tasks.Event')),
                ('content', models.CharField(max_length=200, default='')),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(verbose_name='date published')),
                ('name', models.CharField(max_length=70, default='')),
                ('summry', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequirementTask',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=70, default='')),
                ('state_kind', models.CharField(max_length=1, choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')], default='C')),
                ('priority_lvl', models.CharField(max_length=1, choices=[('C', 'Critical'), ('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='L')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('requirementtask_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='tasks.RequirementTask')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
            },
            bases=('tasks.requirementtask',),
        ),
        migrations.CreateModel(
            name='StateChange',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='tasks.Event')),
                ('new_state', models.CharField(max_length=1, choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')], default='C')),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('requirementtask_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, parent_link=True, to='tasks.RequirementTask')),
                ('milestone', models.ForeignKey(to='tasks.Milestone')),
                ('projects', models.ForeignKey(to='tasks.Requirement')),
            ],
            options={
            },
            bases=('tasks.requirementtask',),
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='project_tast_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='milestone',
            name='event',
            field=models.ForeignKey(to='tasks.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='event_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='requirement_task',
            field=models.ForeignKey(to='tasks.RequirementTask'),
            preserve_default=True,
        ),
    ]
