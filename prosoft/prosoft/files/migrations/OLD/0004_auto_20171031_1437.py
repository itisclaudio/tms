# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_country_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='application',
            name='opening',
        ),
        migrations.RemoveField(
            model_name='application',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='process',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='process',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='opening',
            name='applicants',
        ),
        migrations.AlterField(
            model_name='applicant',
            name='work_status',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1'), (b'4', b'Not Authorized')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='contract',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Full time/Direct'), (b'2', b'Contract to hire'), (b'3', b'Contract')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='work_auth',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1')]),
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='Process',
        ),
    ]
