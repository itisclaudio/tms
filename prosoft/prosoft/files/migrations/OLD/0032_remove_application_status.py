# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0031_application_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='status',
        ),
    ]
