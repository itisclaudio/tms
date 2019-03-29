# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0019_profile_skills_sec'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
