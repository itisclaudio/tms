# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0030_auto_20171219_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
