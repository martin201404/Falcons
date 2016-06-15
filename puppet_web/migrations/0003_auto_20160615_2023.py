# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puppet_web', '0002_role_to_host_usergroup_to_model'),
    ]

    operations = [
        migrations.DeleteModel(
            name='usergroup_to_host',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role_name',
        ),
        migrations.RemoveField(
            model_name='user_group',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='user_group',
            field=models.ForeignKey(blank=True, to='puppet_web.User_group', null=True),
        ),
    ]
