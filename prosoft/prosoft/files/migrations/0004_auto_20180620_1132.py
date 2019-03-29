# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20180601_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='work_status',
            field=models.CharField(default=b'3', max_length=1, choices=[(b'1', b'USC'), (b'2', b'GC'), (b'3', b'H1'), (b'4', b'EAD'), (b'5', b'TN'), (b'9', b'Not Authorized')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='contract',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'FT'), (b'2', b'C2C'), (b'3', b'Contract')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='work_auth',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'USC'), (b'2', b'GC'), (b'3', b'H1'), (b'4', b'EAD'), (b'5', b'TN')]),
        ),
    ]
