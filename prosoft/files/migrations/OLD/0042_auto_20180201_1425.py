# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0041_auto_20180201_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='contacname',
        ),
        migrations.AddField(
            model_name='vendor',
            name='contactname',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
