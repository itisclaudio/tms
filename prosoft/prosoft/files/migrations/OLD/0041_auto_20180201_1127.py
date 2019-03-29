# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0040_auto_20180129_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('contacname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=90, null=True, blank=True)),
                ('phone', models.CharField(max_length=35, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='application',
            name='endclient',
        ),
        migrations.RemoveField(
            model_name='opening',
            name='vendorinfo',
        ),
        migrations.AddField(
            model_name='opening',
            name='vendor',
            field=models.ForeignKey(blank=True, to='files.Vendor', null=True),
        ),
    ]
