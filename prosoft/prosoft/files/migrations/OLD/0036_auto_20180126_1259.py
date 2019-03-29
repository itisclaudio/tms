# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0035_remove_applicant_salary_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='opening',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
