# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0020_profile_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-datetime', 'applicant')},
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(unique=True, max_length=75),
        ),
    ]
