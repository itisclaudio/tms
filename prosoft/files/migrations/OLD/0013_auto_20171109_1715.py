# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0012_application_recruiter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='applicantion',
            new_name='application',
        ),
    ]
