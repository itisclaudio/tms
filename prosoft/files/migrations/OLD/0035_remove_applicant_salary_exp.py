# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0034_auto_20180126_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='salary_exp',
        ),
    ]
