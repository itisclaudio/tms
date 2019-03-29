# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0038_auto_20180126_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
