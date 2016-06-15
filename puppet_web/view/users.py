#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from puppet_web .forms import AddUserForm,LoginUserForm,ChangePasswordForm,PermissionListForm,AddUserGroupForm
from django.contrib.auth import get_user_model,authenticate
from puppet_web.lib.base import autopag
from puppet_web.models import User,PermissionList,RoleList,User_group,role,puppet_host,role_to_host
from django.contrib import auth
from puppet_web.view.Permission import PermissionVerify
def LoginUser(request):
    '''用户登录view'''
    #if request.user.is_authenticated():
    #    return HttpResponseRedirect('/')

    # if request.method == 'GET' and request.GET.has_key('next'):
    #     next = request.GET['next']
    # else:
    #     next = '/'

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))
    else:
        form = LoginUserForm(request)

    kwvars = {
        'request':request,
        'form':form,
        #'next':next,
    }

    return render_to_response('login.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify
def ChangePassword(request):
    if request.method=='POST':
        form = ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logout'))
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('user_chenagepassword.html',kwvars,RequestContext(request))


@login_required()
def AddUser(request):

    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            form.save()
            #return HttpResponseRedirect(reverse('listuser'))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AddUserForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('user_add.html',kwvars,RequestContext(request))
@login_required()
def ListUser(request):

    mod = User
    show_lines = autopag(request,mod)
    return  render_to_response('user_list.html',{'show_lines':show_lines},context_instance=RequestContext(request))

#from puppet_web_admin .forms import AddUserGroupForm
@login_required()
def AddUserGroup(request):
    if request.method =='POST':
        form = AddUserGroupForm(request.POST)
        if form.is_valid():
           form.save()
           return HttpResponseRedirect(reverse('list_user'))
    else:
        form = AddUserGroupForm()
    kwvars ={
        'form':form
    }
    return render_to_response('user_group_add.html',kwvars,context_instance=RequestContext(request))
@login_required()
def User_update(request,id):
     user_update_st=get_object_or_404(User,pk=int(id))
     if request.method=="POST":
            form=AddUserForm(request.POST,instance=user_update_st)
            if form.is_valid():

                form.save()

                return HttpResponseRedirect(reverse("list_user"))
     return render_to_response('user_add.html', {'form': AddUserForm(instance=user_update_st)},context_instance=RequestContext(request))

@login_required()
def UserGrouplist(request):
    mod=User_group
    show_lines = autopag(request,mod)
    return  render_to_response('user_group_list.html',{'show_lines':show_lines},context_instance=RequestContext(request))

@login_required()
def permission_add(request):
    if request.method=='POST':
        form=PermissionListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permissionlist'))
    else:
        form = PermissionListForm()
    kwvars = {
        'form':form,
        # 'request':request,
    }
    return render_to_response('user_permission_add.html',kwvars,context_instance=RequestContext(request))
@login_required()
def permission_list(request):
    #mList = get_user_model().objects.all()
    mod = PermissionList
    show_lines = autopag(request,mod)
    return  render_to_response('user_permission_list.html',{'show_lines':show_lines},context_instance=RequestContext(request))

@login_required()
def permission_deny(request):
    return render_to_response('user_permission_deny.html')

@login_required()
def role_list(request):

    mod = role
    show_lines = autopag(request,mod)
    return  render_to_response('role_list.html',{'show_lines':show_lines},context_instance=RequestContext(request))


from puppet_web.forms import RoleListForm,RoleForm
@login_required()

def role_add(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        #if form.is_valid():
        user_group=request.POST.getlist('user_group')
        role_name=request.POST.get('role_name')
        role_status=request.POST.get('role_status')
        host_id=request.POST.getlist('host_name')

        for u_group in user_group:
            obj = role(role_name=role_name,user_group=u_group,role_status=role_status)
            obj.save()
            for h_id in host_id:

                [h_id_tmp for h_id_tmp  in puppet_host.objects.filter(name=h_id).values_list('id',flat=True)]
                [r_id_tmp for r_id_tmp in role.objects.filter(role_name=role_name).values_list('id',flat=True)]
                print "host %s +++++++++ to role %s " %(h_id_tmp,r_id_tmp)
                obj1 = role_to_host(role_name_id=r_id_tmp,host_id=h_id_tmp)
                obj1.save()
            #form.save()
        return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('role_add.html',kwvars,RequestContext(request))

@login_required()
def role_delete (request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        role_st=get_object_or_404(role,pk=int(id))
        role_st.delete()
        return HttpResponseRedirect(reverse("role_list"))

@login_required()
def role_update (request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        role_update_st=get_object_or_404(role,pk=int(id))
        if request.method=="POST":
            form=RoleForm(request.POST,instance=role_update_st)
            if form.is_valid():

                form.save()

                return HttpResponseRedirect(reverse("role_list"))
        return render_to_response('role_add.html', {'form': RoleForm(instance=role_update_st)},context_instance=RequestContext(request))