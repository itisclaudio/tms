# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_auto_20171103_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicantskills',
            options={'ordering': ('applicant', 'skill')},
        ),
        migrations.RenameField(
            model_name='process',
            old_name='applicant',
            new_name='applicantion',
        ),
        migrations.AlterField(
            model_name='applicant',
            name='relocation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Status-'), (b'1', b'New'), (b'2', b'Ongoing'), (b'3', b'Ended')]),
        ),
    ]
