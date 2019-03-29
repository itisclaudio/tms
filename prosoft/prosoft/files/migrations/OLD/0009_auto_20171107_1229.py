# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_auto_20171107_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='applicantion',
        ),
        migrations.RemoveField(
            model_name='process',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='application',
            name='recruiter',
        ),
        migrations.DeleteModel(
            name='Process',
        ),
    ]
