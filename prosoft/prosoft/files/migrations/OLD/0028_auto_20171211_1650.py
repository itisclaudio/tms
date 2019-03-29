# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0027_auto_20171207_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='education',
            field=models.CharField(default=b'2', max_length=1, null=True, blank=True, choices=[(b'', b'-Education level-'), (b'1', b'High School'), (b'2', b"Bachelor's Degree"), (b'3', b"Master's"), (b'4', b'PHD')]),
        ),
        migrations.AddField(
            model_name='opening',
            name='level',
            field=models.CharField(default=b'2', max_length=1, null=True, blank=True, choices=[(b'', b'-Select Level-'), (b'1', b'Entry'), (b'2', b'Intermediate '), (b'3', b'senior ')]),
        ),
        migrations.AddField(
            model_name='opening',
            name='posted',
            field=models.DateField(default=django.utils.timezone.now, blank=True),
        ),
    ]
