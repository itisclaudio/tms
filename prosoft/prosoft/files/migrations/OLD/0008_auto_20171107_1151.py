# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20171107_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('applicant', 'skill'),
            },
        ),
        migrations.RemoveField(
            model_name='applicantskills',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='applicantskills',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='skills',
        ),
        migrations.AlterField(
            model_name='application',
            name='profile',
            field=models.ForeignKey(to='files.Profile'),
        ),
        migrations.AlterField(
            model_name='opening',
            name='applicantions',
            field=models.ManyToManyField(related_name='applicantions', through='files.Application', to='files.Profile', blank=True),
        ),
        migrations.DeleteModel(
            name='ApplicantSkills',
        ),
        migrations.AddField(
            model_name='profile',
            name='applicant',
            field=models.ForeignKey(to='files.Applicant'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill',
            field=models.ForeignKey(to='files.Skill'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='profiles',
            field=models.ManyToManyField(related_name='profiles', through='files.Profile', to='files.Skill', blank=True),
        ),
    ]
