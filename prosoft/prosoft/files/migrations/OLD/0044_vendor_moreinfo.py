# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0043_auto_20180201_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='moreinfo',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
    ]
