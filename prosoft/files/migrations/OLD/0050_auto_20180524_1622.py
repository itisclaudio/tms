# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0049_auto_20180524_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.IntegerField(default=3, null=True, blank=True, choices=[(0, b'Developer'), (1, b'Admin'), (2, b'Manager'), (3, b'Recruiter')]),
        ),
    ]
