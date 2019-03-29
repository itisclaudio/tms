# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0039_application_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='endclientinfo',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='partnerinfo',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='vendorinfo',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
