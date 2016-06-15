#-*- coding: utf-8 -*-
"""Falcons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$','puppet_web.view.users.LoginUser',name='root'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    #url(r'^login/','puppet_web.views.login'),
    url(r'^login/','puppet_web.view.users.LoginUser',name='login'),
    url(r'^index/$','puppet_web.views.index',name='index'),
    url(r'^logout/$','puppet_web.views.logout',name='logout'),

    url(r'^puppet_web/$','puppet_web.views.login'),
    #puppet 模块
    url(r'^puppet/$','puppet_web.views.puppet_main',name='puppet_model_add'),
    url(r'^puppet_admin_config/$','puppet_web.views.puppet_admin_config'),
    url(r'^puppet_admin/$','puppet_web.views.puppet_admin_s'),
    url(r'^puppet_c_s/$','puppet_web.views.puppet_admin_c_s',name='puppet_c_s'),
    url(r'^puppet_m_c/$','puppet_web.views.puppet_m_c',name='puppet_model_list'),
    url(r'^puppet_m_update-(?P<id>\d+)/$','puppet_web.views.puppet_m_update',name='puppet_m_update'),
    url(r'^puppet_m_upload/$','puppet_web.views.puppet_m_upload'),
    url(r'^puppet_mod_file_list/$','puppet_web.views.puppet_mod_file_list'),
    url(r'^puppet_m_app_1/$','puppet_web.views.puppet_m_app_1'),
    url(r'^puppet_m_app_2/$','puppet_web.views.puppet_m_app_2'),
    url(r'^puppet_m_app_h/$','puppet_web.views.puppet_m_app_h'),
    url(r'^puppet_m_app_g/$','puppet_web.views.puppet_m_app_g'),
    url(r'^puppet_m_d/$','puppet_web.views.puppet_m_d'),

    url(r'^host_group/$','puppet_web.views.host_group'),
    url(r'^host_group_add/$','puppet_web.views.host_group_add'),
    url(r'^host_group_del/$','puppet_web.views.host_group_del'),

    #主机状态
    url(r'^host_list/$','puppet_web.views.host_list',name='host_list'),
    url(r'^puppet_mod_note_d/$','puppet_web.views.puppet_mod_note_d'),
    url(r'^host_add/$','puppet_web.views.host_add',name='host_add'),
    url(r'^host_update-(?P<id>\d+)/$','puppet_web.views.host_update',name='host_update'),
    url(r'^host_delete-(?P<id>\d+)/$','puppet_web.views.host_delete',name='host_delete'),
    #idc local
    url(r'^idc_list/$','puppet_web.views.idc_list',name='idc_list'),
    url(r'^idc_add/$','puppet_web.views.idc_add',name='idc_add'),
    url(r'^idc_update-(?P<id>\d+)/$','puppet_web.views.idc_update',name='idc_update'),
    url(r'^idc_delete-(?P<id>\d+)/$','puppet_web.views.idc_delete',name='idc_delete'),
    #salt

    url(r'^salt_app_g/$','puppet_web.views.salt_app_g'),
    url(r'^salt_app_h/$','puppet_web.views.salt_app_h'),

    url(r'salt_master_list/$','puppet_web.views.salt_master_list',name='salt_master_list'),
    url(r'salt_master_add/$','puppet_web.views.salt_master_add',name='salt_master_add'),
    url(r'salt_master_update-(?P<id>\d+)/$','puppet_web.views.salt_master_update',name='salt_master_update'),
    url(r'salt_master_delete-(?P<id>\d+)/$','puppet_web.views.salt_master_delete',name='salt_master_delete'),
    url(r'salt_re_list/$','puppet_web.views.salt_re_list',name='salt_re_list'),
    ###user manaster
    url(r'^user_add/$','puppet_web.view.users.AddUser',name='add_user'),
    url(r'^user_list/$','puppet_web.view.users.ListUser',name='list_user'),
    url(r'^user_changep/$','puppet_web.view.users.ChangePassword',name='changepassword'),
    url(r'^user_update-(?P<id>\d+)/$','puppet_web.view.users.User_update',name='user_update'),
    ###
    url(r'^user_group_add/$','puppet_web.view.users.AddUserGroup',name='UserGroupadd'),
    url(r'^user_group_list/$','puppet_web.view.users.UserGrouplist',name='UserGrouplist'),

    url(r'^permission_deny/$','puppet_web.view.users.permission_deny',name='permissiondeny'),
    url(r'^permission_add/$','puppet_web.view.users.permission_add',name='permissionadd'),
    url(r'^permission_list/$','puppet_web.view.users.permission_list',name='permissionlist'),

    ###role
    url(r'^role_list/$','puppet_web.view.users.role_list',name='role_list'),
    url(r'^role_add/$','puppet_web.view.users.role_add',name='role_add'),
    url(r'^role_update-(?P<id>\d+)/$','puppet_web.view.users.role_update',name='role_update'),
    url(r'^role_delete-(?P<id>\d+)/$','puppet_web.view.users.role_delete',name='role_delete'),

]

