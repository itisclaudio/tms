# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=75)),
                ('lastname', models.CharField(max_length=75)),
                ('dob', models.DateField(null=True, blank=True)),
                ('phone_home', models.CharField(max_length=15, null=True, blank=True)),
                ('phone_mobile', models.CharField(max_length=15, null=True, blank=True)),
                ('phone_work', models.CharField(max_length=15, null=True, blank=True)),
                ('phone_ex', models.CharField(max_length=6, null=True, blank=True)),
                ('availability', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('location', models.CharField(max_length=25, null=True, blank=True)),
                ('relocation', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=175, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('lastname', 'firstname'),
            },
        ),
        migrations.CreateModel(
            name='ApplicantSkills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
                ('likes', models.BooleanField(default=True)),
                ('applicant', models.ForeignKey(to='files.Applicant')),
            ],
            options={
                'ordering': ('skill',),
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('description', models.TextField(max_length=4000, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='applicantskills',
            name='skill',
            field=models.ForeignKey(to='files.Skill'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='skills',
            field=models.ManyToManyField(related_name='skills', through='files.ApplicantSkills', to='files.Skill', blank=True),
        ),
    ]
