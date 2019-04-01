# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0018_auto_20171127_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skills_sec',
            field=models.ManyToManyField(related_name='skills_sec', to='files.Skill', blank=True),
        ),
    ]
