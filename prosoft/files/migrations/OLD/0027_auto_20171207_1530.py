# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0026_auto_20171206_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='model_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
