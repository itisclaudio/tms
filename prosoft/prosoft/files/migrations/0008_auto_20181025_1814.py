# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_remove_tracking_ulr'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracking',
            name='extrainfo',
            field=models.TextField(max_length=4000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='type',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Changed'), (b'2', b'New'), (b'3', b'Deleted')]),
        ),
    ]
