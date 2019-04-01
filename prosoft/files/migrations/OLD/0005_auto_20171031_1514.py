# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0004_auto_20171031_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'New'), (b'2', b'Ongoing'), (b'3', b'Ended')])),
                ('opening', models.ForeignKey(to='files.Opening')),
                ('profile', models.ForeignKey(to='files.ApplicantSkills')),
            ],
            options={
                'ordering': ('status', '-datetime'),
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Phone call'), (b'2', b'In Person'), (b'3', b'No Interaction')])),
                ('notes', models.TextField(max_length=4000, null=True, blank=True)),
                ('applicant', models.ForeignKey(to='files.Application')),
                ('recruiter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AddField(
            model_name='application',
            name='recruiter',
            field=models.ManyToManyField(related_name='recruiter', through='files.Process', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='applicantions',
            field=models.ManyToManyField(related_name='applicantions', through='files.Application', to='files.ApplicantSkills', blank=True),
        ),
    ]
