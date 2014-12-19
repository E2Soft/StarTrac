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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('event_kind', models.CharField(default='C', choices=[('C', 'Accepted'), ('P', 'Created')], max_length=1)),
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
                ('event_ptr', models.OneToOneField(to='tasks.Event', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
                ('content', models.CharField(default='', max_length=200)),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(verbose_name='date published')),
                ('name', models.CharField(default='', max_length=70)),
                ('summry', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequirementTask',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=70)),
                ('state_kind', models.CharField(default='C', choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')], max_length=1)),
                ('priority_lvl', models.CharField(default='L', choices=[('C', 'Critical'), ('H', 'High'), ('M', 'Medium'), ('L', 'Low')], max_length=1)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('content', models.CharField(default='', max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('requirementtask_ptr', models.OneToOneField(to='tasks.RequirementTask', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
            ],
            options={
            },
            bases=('tasks.requirementtask',),
        ),
        migrations.CreateModel(
            name='StateChange',
            fields=[
                ('event_ptr', models.OneToOneField(to='tasks.Event', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
                ('new_state', models.CharField(default='C', choices=[('P', 'Accepted'), ('C', 'Created'), ('Z', 'Closed'), ('O', 'On Wait')], max_length=1)),
            ],
            options={
            },
            bases=('tasks.event',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('requirementtask_ptr', models.OneToOneField(to='tasks.RequirementTask', auto_created=True, primary_key=True, parent_link=True, serialize=False)),
                ('assigned_to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('milestone', models.ForeignKey(null=True, blank=True, to='tasks.Milestone')),
                ('projects', models.ForeignKey(null=True, blank=True, to='tasks.Requirement')),
            ],
            options={
            },
            bases=('tasks.requirementtask',),
        ),
        migrations.AddField(
            model_name='requirementtask',
            name='project_tast_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='milestone',
            name='event',
            field=models.ForeignKey(null=True, to='tasks.Event'),
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
