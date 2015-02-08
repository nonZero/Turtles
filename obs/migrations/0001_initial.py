# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import obs.models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TurtleObservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observer', models.CharField(max_length=50, verbose_name='Observer', db_index=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Phone', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('date', models.DateField(db_index=True, null=True, verbose_name='Observation Date', blank=True)),
                ('time', models.TimeField(db_index=True, null=True, verbose_name='Observation Time', blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=2039, null=True, verbose_name='point', blank=True)),
                ('point_accuracy', models.FloatField(null=True, blank=True)),
                ('alive', models.IntegerField(default=1, verbose_name='Turtle Status', choices=[(4, 'Unknown'), (2, 'Injured Turtle'), (1, 'Live Turtle'), (0, 'Dead Turtle')])),
                ('location', models.IntegerField(default=1, verbose_name='Turtle Place', choices=[(1, 'On the shore'), (2, 'At Sea level, less than 5m deep'), (3, 'Deeper than 5m deep'), (4, 'On the Sea bottom')])),
                ('species', models.IntegerField(default=3, verbose_name='Turtle Species', choices=[(3, 'Unknown'), (1, 'Chelonia mydas, Green Sea Turtle'), (2, 'Carette caretta, Loggerhead Sea Turtle'), (4, 'Eretmochelys imbricata, Hawksbill Sea Turtle'), (5, 'Dermochelys coriacea, Leatherback Sea Turtle'), (6, 'Trionyx triunguis, Nile Soft Shell Turtle'), (7, 'Mauremys caspica, Caspian Turtle')])),
                ('behaviour', models.IntegerField(blank=True, null=True, verbose_name='Turtle Behaviour', choices=[(1, 'Breathing'), (2, 'Breeding'), (3, 'Feeding'), (4, 'Nesting'), (5, 'Sleeping'), (6, 'Swimming'), (7, 'Other')])),
                ('tail_length', models.IntegerField(default=0, verbose_name='Tail Length', choices=[(0, 'Unknown'), (1, 'Long'), (2, 'Short')])),
                ('comment', models.TextField(help_text='Anything else you want to tell us? Did the turtle have a tag on it?', null=True, verbose_name='Observation Description', blank=True)),
                ('uid', models.CharField(default=obs.models.make_uid, max_length=12)),
                ('email_uid', models.CharField(default=obs.models.make_email_uid, max_length=6)),
            ],
            options={
                'verbose_name': 'turtle observation',
                'verbose_name_plural': 'turtle observations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurtleObservationEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('sender', models.EmailField(max_length=75, null=True, blank=True)),
                ('subject', models.TextField(null=True, blank=True)),
                ('body_text', models.EmailField(max_length=75, null=True, blank=True)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('ob', models.ForeignKey(related_name='emails', to='obs.TurtleObservation')),
            ],
            options={
                'verbose_name': 'turtle observation email',
                'verbose_name_plural': 'turtle observation emails',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurtleObservationPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('img', models.ImageField(height_field='height', width_field='width', upload_to='reports')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('original_filename', models.CharField(max_length=500, null=True, blank=True)),
                ('email', models.ForeignKey(related_name='photos', blank=True, to='obs.TurtleObservationEmail', null=True)),
                ('ob', models.ForeignKey(related_name='photos', to='obs.TurtleObservation')),
            ],
            options={
                'verbose_name': 'turtle observation photo',
                'verbose_name_plural': 'turtle observation photos',
            },
            bases=(models.Model,),
        ),
    ]
