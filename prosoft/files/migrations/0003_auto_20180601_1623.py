# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_member_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='work_status',
            field=models.CharField(default=b'3', max_length=1, choices=[(b'1', b'USC: US Citizen'), (b'2', b'GC: Greencard'), (b'3', b'H1'), (b'4', b'EAD'), (b'5', b'TN'), (b'9', b'Not Authorized')]),
        ),
        migrations.AlterField(
            model_name='applicant_doc',
            name='type',
            field=models.CharField(default=b'2', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'RTR (Right to Represent)'), (b'2', b'Visa'), (b'3', b'Photo ID'), (b'4', b'NDA (Non-discloser Agreement)'), (b'5', b'Other')]),
        ),
    ]
