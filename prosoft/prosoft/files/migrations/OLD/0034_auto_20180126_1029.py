# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0033_auto_20180125_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='salary',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='applicant_doc',
            name='type',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'RTR (Right to Represent)'), (b'2', b'Visa copy (H1B, OPT)'), (b'3', b'Photo ID (DL, EAD card)'), (b'4', b'NDA (Non-discloser Agreement)'), (b'5', b'Passport')]),
        ),
    ]
