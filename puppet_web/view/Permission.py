#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required

from puppet_web.models import User,RoleList,PermissionList,role

#from django.contrib.auth.models import Permission


def PermissionVerify(*args, **kwargs):
    '''权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    '''
    def decorator(view_func,*args, **kwargs):
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_superuser:

                    return HttpResponseRedirect(reverse('permissiondeny'))


            else:
                print "permission +++++++++++++++++++++"
                pass

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator

