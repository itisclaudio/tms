# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_auto_20180620_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
