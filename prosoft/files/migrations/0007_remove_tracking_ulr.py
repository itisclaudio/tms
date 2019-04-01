# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_tracking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracking',
            name='ulr',
        ),
    ]
