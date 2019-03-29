# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20171031_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='availability',
            field=models.DateField(default=django.utils.timezone.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='city',
            field=models.CharField(help_text='Enter city', max_length=65, null=True, verbose_name='City', blank=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='righttorep',
            field=models.BooleanField(default=False, verbose_name='Right to Represent'),
        ),
    ]
