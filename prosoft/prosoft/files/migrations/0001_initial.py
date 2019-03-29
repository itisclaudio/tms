# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import prosoft.files.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Phone call'), (b'2', b'In Person'), (b'3', b'No Interaction')])),
                ('notes', models.TextField(max_length=4000, null=True, blank=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=75)),
                ('lastname', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=90, null=True, blank=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('phone_1', models.CharField(max_length=35, null=True, blank=True)),
                ('phone_2', models.CharField(max_length=35, null=True, blank=True)),
                ('work_status', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1'), (b'4', b'Not Authorized')])),
                ('availability', models.DateField(default=django.utils.timezone.now, null=True, blank=True)),
                ('relocation', models.BooleanField(default=False)),
                ('righttorep', models.BooleanField(default=False, verbose_name='Right to Represent')),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('city', models.CharField(help_text='Enter city', max_length=65, null=True, verbose_name='City', blank=True)),
                ('zipcode', models.CharField(max_length=10, null=True, blank=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
                ('usexperience', models.IntegerField(null=True, blank=True)),
                ('education', models.CharField(max_length=200, null=True, blank=True)),
                ('besttime', models.CharField(max_length=200, null=True, blank=True)),
                ('salary_cur', models.CharField(max_length=40, null=True, blank=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('lastname', 'firstname'),
            },
        ),
        migrations.CreateModel(
            name='Applicant_Doc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.FileField(null=True, upload_to=prosoft.files.models.generate_applicant_doc_name, blank=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'RTR (Right to Represent)'), (b'2', b'Visa copy (H1B, OPT)'), (b'3', b'Photo ID (DL, EAD card)'), (b'4', b'NDA (Non-discloser Agreement)'), (b'5', b'Passport')])),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('applicant', models.ForeignKey(to='files.Applicant')),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.CharField(max_length=35, null=True, blank=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('activities', models.ManyToManyField(related_name='activities', through='files.Activity', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('profile', 'opening'),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=2, null=True, blank=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startdate', models.DateField(default=django.utils.timezone.now, null=True, blank=True)),
                ('posted', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('role', models.CharField(max_length=75)),
                ('responsibilities', models.TextField(max_length=4000, null=True, blank=True)),
                ('rate', models.CharField(max_length=35, null=True, blank=True)),
                ('city', models.CharField(max_length=65, null=True, blank=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
                ('education', models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Education level-'), (b'1', b'High School'), (b'2', b"Bachelor's"), (b'3', b"Master's"), (b'4', b'PhD')])),
                ('level', models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Level-'), (b'1', b'Entry'), (b'2', b'Intermediate '), (b'3', b'Senior ')])),
                ('contract', models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'Full time/Direct'), (b'2', b'Contract to hire'), (b'3', b'Contract')])),
                ('work_auth', models.CharField(blank=True, max_length=1, null=True, choices=[(b'', b'-Select Type-'), (b'1', b'US Citizen'), (b'2', b'Work Permit/Legal Resident'), (b'3', b'Work Visa/H1')])),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('endclientinfo', models.CharField(max_length=300, null=True, blank=True)),
                ('partnerinfo', models.CharField(max_length=300, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('role',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('salary', models.CharField(max_length=40, null=True, blank=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('applicant', models.ForeignKey(to='files.Applicant')),
            ],
            options={
                'ordering': ('applicant',),
            },
        ),
        migrations.CreateModel(
            name='Profile_Doc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.FileField(null=True, upload_to=prosoft.files.models.generate_doc_name, blank=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'', b'-Select Type-'), (b'1', b'Resume'), (b'2', b'Cover letter'), (b'3', b'Certification'), (b'4', b'Letter of recommendation'), (b'5', b'Other')])),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(to='files.Profile')),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=30, null=True, blank=True)),
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
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=75)),
                ('description', models.TextField(max_length=4000, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
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
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('contactname', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=90, null=True, blank=True)),
                ('phone', models.CharField(max_length=35, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('moreinfo', models.CharField(max_length=400, null=True, blank=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='files.Skill'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills_sec',
            field=models.ManyToManyField(related_name='skills_sec', to='files.Skill', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='applications',
            field=models.ManyToManyField(related_name='applications', through='files.Application', to='files.Profile', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='skills',
            field=models.ManyToManyField(related_name='open_skills_main', to='files.Skill', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='skills_sec',
            field=models.ManyToManyField(related_name='open_skills_sec', to='files.Skill', blank=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='state',
            field=models.ForeignKey(blank=True, to='files.State', null=True),
        ),
        migrations.AddField(
            model_name='opening',
            name='vendor',
            field=models.ForeignKey(blank=True, to='files.Vendor', null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='opening',
            field=models.ForeignKey(to='files.Opening'),
        ),
        migrations.AddField(
            model_name='application',
            name='profile',
            field=models.ForeignKey(to='files.Profile'),
        ),
        migrations.AddField(
            model_name='application',
            name='recruiter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
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
        migrations.AddField(
            model_name='activity',
            name='application',
            field=models.ForeignKey(to='files.Application'),
        ),
        migrations.AddField(
            model_name='activity',
            name='recruiter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('profile', 'opening')]),
        ),
    ]
