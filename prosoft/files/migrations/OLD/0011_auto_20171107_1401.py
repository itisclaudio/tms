# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0010_auto_20171107_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='recruiter',
        ),
        migrations.AddField(
            model_name='application',
            name='activities',
            field=models.ManyToManyField(related_name='activities', through='files.Activity', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
