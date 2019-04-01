# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0025_auto_20171202_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=30)),
                ('field_id', models.IntegerField(null=True, blank=True)),
                ('content', models.TextField(max_length=4000, null=True, blank=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('private', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('recruiter', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AlterModelOptions(
            name='opening',
            options={'ordering': ('role',)},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('applicant',)},
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Status-'), (b'1', b'New'), (b'2', b'Active'), (b'3', b'Inactive')]),
        ),
    ]
