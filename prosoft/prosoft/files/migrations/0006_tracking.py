# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0005_opening_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Change'), (b'2', b'Add'), (b'3', b'Delete')])),
                ('entity', models.CharField(max_length=45, null=True, blank=True)),
                ('entity_id', models.IntegerField(null=True, blank=True)),
                ('entity_field', models.CharField(max_length=45, null=True, blank=True)),
                ('ulr', models.CharField(max_length=99, null=True, blank=True)),
                ('old', models.TextField(max_length=4000, null=True, blank=True)),
                ('new', models.TextField(max_length=4000, null=True, blank=True)),
                ('show', models.BooleanField(default=True)),
                ('recruiter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
    ]
