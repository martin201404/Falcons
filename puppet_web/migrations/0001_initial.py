# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=40, db_index=True)),
                ('email', models.EmailField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=64, null=True)),
                ('sex', models.CharField(max_length=2, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choices_host_group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=300, null=True, verbose_name='\u7ec4\u540d')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='\u4e3b\u673aip', blank=True)),
                ('idc', models.CharField(max_length=200, null=True, verbose_name='idc')),
            ],
        ),
        migrations.CreateModel(
            name='idc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idc_name', models.CharField(max_length=200, null=True, verbose_name='idc name')),
                ('idc_floor', models.CharField(max_length=10, null=True, verbose_name='\u697c\u5c42')),
                ('idc_cabinets', models.CharField(max_length=10, null=True, verbose_name='\u673a\u67dc')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('group_name', models.ManyToManyField(to='puppet_web.Choices_host_group', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='puppet_admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('puppet_model_path', models.CharField(max_length=100, null=True, verbose_name='puppet\u6a21\u5757\u8def\u5f84')),
                ('puppet_files_server_path', models.CharField(max_length=100, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u670d\u52a1\u5668')),
                ('puppet_config_path', models.CharField(max_length=200, null=True, verbose_name='puppet \u914d\u7f6e\u6587\u4ef6')),
                ('puppet_server_ip', models.CharField(max_length=50, null=True, verbose_name='puppet ip')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='puppet_edit_config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=50, null=True, verbose_name='\u6a21\u5757\u540d\u5b57')),
                ('file_name', models.CharField(max_length=20, null=True, verbose_name='\u6587\u4ef6\u540d')),
                ('contents', models.TextField(max_length=10000000, null=True, verbose_name='\u5185\u5bb9', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='puppet_host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='ip \u5730\u5740', blank=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('status', models.CharField(max_length=3, verbose_name='\u4e3b\u673a\u72b6\u6001', choices=[(b'on', b'on'), (b'off', b'off')])),
                ('os_varsion', models.CharField(max_length=10, verbose_name='\u64cd\u4f5c\u7cfb\u7edf', choices=[(b'Centos', b'Centos'), (b'FreeBSD', b'FreeBSD'), (b'RedHat', b'RedHat'), (b'Debian', b'Debian'), (b'Ubuntu', b'Ubuntu'), (b'Gentoo', b'Gentoo'), (b'OpenSUSE', b'OpenSUSE')])),
                ('idc_floor', models.CharField(max_length=4, null=True, verbose_name='\u697c\u5c42', blank=True)),
                ('idc_cabinets', models.CharField(max_length=10, null=True, verbose_name='\u673a\u67dc\u53f7', blank=True)),
                ('group_name', models.ForeignKey(related_name='group_name_group_name', blank=True, to='puppet_web.Choices_host_group', null=True)),
                ('idc_name', models.ForeignKey(blank=True, to='puppet_web.idc', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='puppet_mod_file_upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=50, null=True, verbose_name='\u6a21\u5757\u540d')),
                ('file', models.FileField(upload_to=b'')),
                ('describe', models.TextField(max_length=200, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='puppet_mod_group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mod_name', models.CharField(max_length=100, null=True, verbose_name='\u6a21\u5757\u540d')),
                ('mod_group', models.CharField(max_length=200, null=True, verbose_name='\u4e3b\u673a\u7ec4')),
            ],
        ),
        migrations.CreateModel(
            name='puppet_mod_host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mod_name', models.CharField(max_length=100, null=True, verbose_name='\u6a21\u5757\u540d')),
                ('mod_host', models.CharField(max_length=200, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='ipv4', blank=True)),
                ('group_name', models.CharField(max_length=50, null=True, verbose_name='\u4e3b\u673a\u7ec4')),
            ],
        ),
        migrations.CreateModel(
            name='puppet_models',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=200, null=True, verbose_name='model name')),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_name', models.CharField(max_length=30, null=True, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('user_group', models.CharField(max_length=30, null=True, verbose_name='\u7528\u6237\u7ec4')),
                ('role_status', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoleList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('group_name', models.ManyToManyField(to='puppet_web.PermissionList', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='salt_admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='salt master ip', blank=True)),
                ('salt_name', models.CharField(max_length=50, null=True, verbose_name='salt master \u4e3b\u673a\u540d')),
                ('local', models.CharField(max_length=200, null=True, verbose_name='salt master \u4f4d\u7f6e')),
            ],
        ),
        migrations.CreateModel(
            name='salt_main',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salt_name', models.ForeignKey(to='puppet_web.salt_admin')),
            ],
        ),
        migrations.CreateModel(
            name='salt_run_command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=1500, null=True, verbose_name='command')),
                ('run_time', models.DateTimeField(auto_now=True, verbose_name='\u8fd0\u884c\u65f6\u95f4 ')),
                ('run_user', models.CharField(max_length=40, null=True, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='User_group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_group', models.CharField(max_length=40, null=True, verbose_name='\u7528\u6237\u7ec4')),
                ('username', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='usergroup_to_host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_group_id', models.PositiveIntegerField(null=True)),
                ('host_id', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='puppet_host',
            name='salt_name',
            field=models.ForeignKey(blank=True, to='puppet_web.salt_admin', null=True),
        ),
        migrations.AddField(
            model_name='choices_host_group',
            name='role_name',
            field=models.ForeignKey(blank=True, to='puppet_web.role', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='role_name',
            field=models.ForeignKey(blank=True, to='puppet_web.role', null=True),
        ),
    ]
