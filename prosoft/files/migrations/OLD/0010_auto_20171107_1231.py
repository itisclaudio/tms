# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0009_auto_20171107_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Phone call'), (b'2', b'In Person'), (b'3', b'No Interaction')])),
                ('notes', models.TextField(max_length=4000, null=True, blank=True)),
                ('applicantion', models.ForeignKey(to='files.Application')),
                ('recruiter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AddField(
            model_name='application',
            name='recruiter',
            field=models.ManyToManyField(related_name='recruiter', through='files.Activity', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
