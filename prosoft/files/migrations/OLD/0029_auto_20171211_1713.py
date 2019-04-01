# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0028_auto_20171211_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='contract',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'Full time/Direct'), (b'2', b'Contract to hire'), (b'3', b'Contract')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='education',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Education level-'), (b'1', b'High School'), (b'2', b"Bachelor's Degree"), (b'3', b"Master's"), (b'4', b'PHD')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='level',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Level-'), (b'1', b'Entry'), (b'2', b'Intermediate '), (b'3', b'Senior ')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='work_auth',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1')]),
        ),
    ]
