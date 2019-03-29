# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import prosoft.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0015_auto_20171122_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_Doc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.FileField(null=True, upload_to=prosoft.files.models.generate_doc_name, blank=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Resume'), (b'2', b'Cover letter')])),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('profile', '-datetime'),
            },
        ),
        migrations.RemoveField(
            model_name='profile',
            name='resume',
        ),
        migrations.AddField(
            model_name='profile_doc',
            name='profile',
            field=models.ForeignKey(to='files.Profile'),
        ),
    ]
