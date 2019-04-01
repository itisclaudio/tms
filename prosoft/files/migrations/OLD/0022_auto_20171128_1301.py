# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0021_auto_20171128_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='skills',
            field=models.ManyToManyField(related_name='open_skills_main', to='files.Skill', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='skills_sec',
            field=models.ManyToManyField(related_name='open_skills_sec', to='files.Skill', blank=True),
        ),
    ]
