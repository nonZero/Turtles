# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import obs.models


class Migration(migrations.Migration):

    dependencies = [
        ('obs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turtleobservation',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True, verbose_name='Observation Date', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='turtleobservation',
            name='email_uid',
            field=models.CharField(default=obs.models.make_email_uid, unique=True, max_length=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='turtleobservation',
            name='uid',
            field=models.CharField(default=obs.models.make_uid, unique=True, max_length=12),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='turtleobservationemail',
            name='body_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='turtleobservationphoto',
            name='img',
            field=models.ImageField(height_field='height', upload_to='reports', width_field='width', verbose_name='image'),
            preserve_default=True,
        ),
    ]
