# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0036_auto_20180126_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='application',
            name='submited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='application',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
