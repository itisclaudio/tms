# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0029_auto_20171211_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ('profile', 'opening')},
        ),
        migrations.AlterField(
            model_name='opening',
            name='startdate',
            field=models.DateField(default=django.utils.timezone.now, null=True, blank=True),
        ),
    ]
