# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0017_auto_20171126_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('applicant',)},
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='profiles',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='skill',
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='files.Skill', blank=True),
        ),
    ]
