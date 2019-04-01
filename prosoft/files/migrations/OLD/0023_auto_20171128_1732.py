# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0022_auto_20171128_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='contract',
            field=models.CharField(default=b'1', max_length=1, null=True, blank=True, choices=[(b'', b'-Select Type-'), (b'1', b'Full time/Direct'), (b'2', b'Contract to hire'), (b'3', b'Contract')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='work_auth',
            field=models.CharField(default=b'1', max_length=1, null=True, blank=True, choices=[(b'', b'-Select Type-'), (b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1')]),
        ),
    ]
