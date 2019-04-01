# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0032_remove_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='applicant',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='opening',
            name='education',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Education level-'), (b'1', b'High School'), (b'2', b"Bachelor's"), (b'3', b"Master's"), (b'4', b'PhD')]),
        ),
        migrations.AlterField(
            model_name='profile_doc',
            name='type',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'Resume'), (b'2', b'Cover letter'), (b'3', b'Certification'), (b'4', b'Letter of recommendation'), (b'5', b'Other')]),
        ),
    ]
