# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0037_auto_20180126_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='submited',
        ),
        migrations.AddField(
            model_name='application',
            name='endclient',
            field=models.CharField(max_length=99, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='application',
            name='rate',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
    ]
