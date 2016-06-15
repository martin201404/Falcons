# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puppet_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='role_to_host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_name_id', models.PositiveIntegerField(null=True)),
                ('host_id', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='usergroup_to_model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_group_id', models.PositiveIntegerField(null=True)),
                ('model_id', models.PositiveIntegerField(null=True)),
            ],
        ),
    ]
