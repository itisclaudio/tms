# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0024_auto_20171130_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opening',
            name='applicantions',
        ),
        migrations.AddField(
            model_name='opening',
            name='applications',
            field=models.ManyToManyField(related_name='applications', through='files.Application', to='files.Profile', blank=True),
        ),
    ]
