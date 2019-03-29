# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default=b'1', max_length=1, choices=[(1, b'New'), (2, b'Ongoing'), (3, b'Ended')])),
            ],
            options={
                'ordering': ('status', '-datetime'),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Opening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startdate', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('role', models.CharField(max_length=75)),
                ('responsibilities', models.TextField(max_length=4000, null=True, blank=True)),
                ('rate', models.CharField(max_length=35, null=True, blank=True)),
                ('city', models.CharField(max_length=65, null=True, blank=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
                ('contract', models.CharField(default=b'1', max_length=1, choices=[(1, b'Full time/Direct'), (2, b'Contract to hire'), (3, b'Contract')])),
                ('work_auth', models.CharField(default=b'1', max_length=1, choices=[(1, b'US Citizen'), (2, b'Work Permit/Legal Resident'), (3, b'Work Visa/H1')])),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('startdate',),
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(1, b'Phone call'), (2, b'In Person'), (3, b'No Interaction')])),
                ('notes', models.TextField(max_length=4000, null=True, blank=True)),
                ('applicant', models.ForeignKey(to='files.Application')),
                ('recruiter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=35)),
                ('code', models.CharField(max_length=2)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='location',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='phone_ex',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='phone_home',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='phone_mobile',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='phone_work',
        ),
        migrations.RemoveField(
            model_name='applicantskills',
            name='likes',
        ),
        migrations.AddField(
            model_name='applicant',
            name='besttime',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='city',
            field=models.CharField(max_length=65, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='education',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='email',
            field=models.EmailField(max_length=90, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='experience',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='phone_1',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='phone_2',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='righttorep',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='salary_cur',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='salary_exp',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='usexperience',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='work_status',
            field=models.CharField(default=b'1', max_length=1, choices=[(1, b'US Citizen'), (2, b'Work Permit/Legal Resident'), (3, b'Work Visa/H1'), (4, b'Not Authorized')]),
        ),
        migrations.AddField(
            model_name='applicant',
            name='zipcode',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='address',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='applicants',
            field=models.ManyToManyField(related_name='applicants', through='files.Application', to='files.Applicant', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='state',
            field=models.ForeignKey(blank=True, to='files.State', null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(to='files.Applicant'),
        ),
        migrations.AddField(
            model_name='application',
            name='opening',
            field=models.ForeignKey(to='files.Opening'),
        ),
        migrations.AddField(
            model_name='application',
            name='recruiter',
            field=models.ManyToManyField(related_name='recruiter', through='files.Process', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='country',
            field=models.ForeignKey(blank=True, to='files.Country', null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='state',
            field=models.ForeignKey(blank=True, to='files.State', null=True),
        ),
    ]
