# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import prosoft.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0014_profile_resume'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('profile', 'opening')]),
        ),
    ]
