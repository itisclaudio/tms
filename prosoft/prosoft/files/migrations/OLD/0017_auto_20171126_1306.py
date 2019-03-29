# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import prosoft.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0016_auto_20171122_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant_Doc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.FileField(null=True, upload_to=prosoft.files.models.generate_applicant_doc_name, blank=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'RTR (Right to Represent)'), (b'2', b'Visa copy (H1B, OPT)'), (b'3', b'Photo ID (DL, EAD card)'), (b'4', b'NDA (Non-discloser Agreement)')])),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('applicant', models.ForeignKey(to='files.Applicant')),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AlterModelOptions(
            name='profile_doc',
            options={'ordering': ('-datetime',)},
        ),
        migrations.AlterField(
            model_name='opening',
            name='contract',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'Full time/Direct'), (b'2', b'Contract to hire'), (b'3', b'Contract')]),
        ),
        migrations.AlterField(
            model_name='opening',
            name='work_auth',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1')]),
        ),
        migrations.AlterField(
            model_name='profile_doc',
            name='type',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'Resume'), (b'2', b'Cover letter')]),
        ),
    ]
