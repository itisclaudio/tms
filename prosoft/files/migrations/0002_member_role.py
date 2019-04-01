# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.IntegerField(default=3, null=True, blank=True, choices=[(0, b'Developer'), (1, b'Admin'), (2, b'Manager'), (3, b'Recruiter')]),
        ),
    ]
