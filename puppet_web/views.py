#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,RequestContext,get_list_or_404,get_object_or_404,_get_queryset
from django.http import HttpResponse,HttpResponseRedirect,Http404

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.contrib import auth,messages
from puppet_web .forms import idcForm,host_addForm,puppet_edit_update,puppet_mod_file_uploadForm,hostgroup_to_idc_local_Form,puppet_from,UserFrom,puppet_admin_modForm,salt_adminmodForm,puppet_edit_confForm,Choices_host_groupForm,host_group_addForm,puppet_mod_groupFrom,puppet_mod_hostForm,puppet_mod_hostForm_h,puppet_mod_groupForm_g
from puppet_web .models import puppet_mod_file_upload,puppet_admin,puppet_host,salt_admin,puppet_edit_config,Choices_host_group,puppet_mod_group,puppet_mod_host,idc,puppet_models
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from  django.middleware.csrf import get_token
from puppet_web.lib.base import autopag,byte_string,ping,check_aliveness
from puppet_web.lib.model import model_new,model_del,model_active_host,model_active_group,mod_disable_host,model_update,host_del
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

import  re,json,os,tempfile

@login_required()
def login(request):
    if request.method == 'POST':
        form = UserFrom()
    #    if form.is_valid():
        username = request.POST.get('usernmae','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
               if user.is_active:
                   auth.login(request,user)
                   return HttpResponseRedirect(reverse("index"))
               else:
                   return HttpResponseRedirect('/')
        else:
               return HttpResponseRedirect('/')
               #return render_to_response('error.html')

    else:
       form = UserFrom()
    return render_to_response('login.html',{'form':form},context_instance=RequestContext(request))

def logout(request):
     auth.logout(request)
     return HttpResponseRedirect(reverse('root'))


def index(request):
     if not request.user.is_authenticated():
         return HttpResponseRedirect('/')
     else:
        host_all_conut= puppet_host.objects.all().count()
        host_active_count = puppet_host.objects.filter(status='on').count()
        puppet_mod_count = puppet_edit_config.objects.all().count()
        return render_to_response("index.html", {'host_all_conut':host_all_conut,'host_active_count':host_active_count,'puppet_mod_count':puppet_mod_count})



'''
puppet model write
'''
@csrf_protect

def puppet_main(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        csrfContext = RequestContext(request)
        if request.method == 'POST':
            form = puppet_edit_confForm(request.POST)
            if form.is_valid():
                csrf_token = get_token(request)

                model_name = form.cleaned_data['model_name']
                file_name = form.cleaned_data['file_name']
                contents = form.cleaned_data['contents']

                obj = puppet_edit_config(model_name=model_name,file_name=file_name,contents=contents)
                obj.save()
                mod_name=model_name
                model_new(request,mod_name,file_name,contents)
                re = puppet_models.objects.filter(model_name=model_name)
                if not re:
                   obj1 = puppet_models(model_name=mod_name)
                   obj1.save()
                else:
                    pass
                return HttpResponseRedirect('/puppet_m_c')
        else:
            form = puppet_edit_confForm()
                #form1 = Choices_host_groupForm()
        return render_to_response('puppet_main.html', {'form': form },RequestContext(request, {}))

def puppet_m_c(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_edit_config
        show_lines = autopag(request,mod)
        return render_to_response('puppet_m_c.html', RequestContext(request, {'show_lines': show_lines,}))

def puppet_m_d(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_edit_config
        show_lines = autopag(request,mod)
        items = puppet_edit_config.objects.all()

        if request.method == 'POST':
            csrf_token = get_token(request)
            id_list = request.POST.getlist('checkbox')
            if not id_list :
                return render_to_response('error.html',{'id':id_list})
            else:

                int_id_list = [int(id) for id in id_list]  # convert to int
                for id in int_id_list :

                   #puppet_edit_config.objects.get(id=id).delete()
                    mod_name_list=puppet_edit_config.objects.all().values_list('model_name',flat=True)
                    for mod_name in mod_name_list:
                        model_del(request,mod_name)
                return HttpResponseRedirect('/puppet_m_c/')

        return render_to_response("puppet_m_d.html",{'items': items,'show_lines': show_lines,},context_instance=RequestContext(request),)
@csrf_protect
def puppet_m_update(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        puppet_update=get_object_or_404(puppet_edit_config,pk=int(id))
        if request.method=="POST":
            form=puppet_edit_update(request.POST,instance=puppet_update)
            if form.is_valid():
                csrf_token = get_token(request)
                puppet_update=form.save()
                file_name=request.POST.get('file_name')
                mod_name=request.POST.get('model_name')
                contents=request.POST.get('contents')
                model_update(request,mod_name,file_name,contents)

                #blog.save()
                return HttpResponseRedirect(reverse("puppet_model_list"))
        return render_to_response('puppet_main.html', {'form': puppet_edit_update(instance=puppet_update)},context_instance=RequestContext(request))

##puppet file upload
def puppet_m_upload(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        form = puppet_mod_file_uploadForm(request.POST, request.FILES)
        if request.method == 'POST':
            # uf = puppet_mod_file_upload(request.POST, request.FILES)
             id_list = request.POST.getlist('choices_model_name')
             if form:
                csrf_token = get_token(request)
                describe=request.POST.get('describe')
                file = request.FILES.get('file',None)  #'uploadfile'与提交表单中input名一致，多个文件参见getlist()
                file_con = file.read()
                f = file.name
                for model_name in id_list:
                 #写入数据库
                    # for f1 in file_con:
                        #print "%s %s %s %s" %(model_name,describe,file,file_con)
                        user = puppet_mod_file_upload()
                        user.model_name = model_name
                        user.file = file
                        user.describe = describe
                        user.save()
                        user.clean()

                        puppet_mod_path1=puppet_admin.objects.all().values_list('puppet_model_path',flat=True)
                        new_file= puppet_mod_file_upload.objects.filter(file='./'+f).values_list('id',flat=True)
                        for puppet_mod_path in puppet_mod_path1:
                           #os.rename('/tmp/'+f,m_path+f)
                           m_path=puppet_mod_path+'/' + model_name+'/files/'+f
                           os.rename('/tmp/'+f,m_path)
                           for n_f in new_file:
                              puppet_mod_file_upload.objects.filter(id=n_f).update(file=puppet_mod_path+'/'+model_name+'/files/'+f)
                        #    print  "cccc %s" %(m_path)
                        #handle_uploaded_file(f,model_name)

                return HttpResponseRedirect('/puppet_mod_file_list/')

             else:
                 print 'upload file error'
        else:

            form = puppet_mod_file_uploadForm()

        return render_to_response('puppet_mod_file_upload.html',{'form':form},context_instance=RequestContext(request),)

def puppet_admin_s(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        form = puppet_admin_modForm()
        if request.method == 'POST':
            form = puppet_admin_modForm(data=request.POST)
            if form.is_valid():
                csrf_token = get_token(request)
                puppet_model_path = form.cleaned_data['puppet_model_path']
                puppet_files_server_path = form.cleaned_data['puppet_files_server_path']
                puppet_config_path = form.cleaned_data['puppet_config_path']
                new = puppet_admin.objects.create(puppet_model_path=puppet_model_path,puppet_files_server_path=puppet_files_server_path,puppet_config_path=puppet_config_path)
                new.save()
                c = {'form': form}
                c.update(csrf(request))
                return render_to_response("puppet_admin.html", c)
                #return render_to_response('puppet_admin.html', {'csrf_token': csrf_token})
        else:
            form = puppet_admin_modForm()

        return render_to_response('puppet_admin.html', {'form': form},context_instance=RequestContext(request))

def puppet_admin_config(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        if request.method == 'POST':
          form = puppet_admin_modForm(request.POST)

          if form.is_valid():
            csrf_token = get_token(request)
            puppet_model_path = form.cleaned_data['puppet_model_path']
            puppet_files_server_path = form.cleaned_data['puppet_files_server_path']
            puppet_config_path = form.cleaned_data['puppet_config_path']
            puppet_server_ip = form.cleaned_data['puppet_server_ip']
            obj = puppet_admin(puppet_model_path=puppet_model_path,puppet_files_server_path=puppet_files_server_path,puppet_config_path=puppet_config_path,puppet_server_ip=puppet_server_ip,id=1)
            obj.save()
            return HttpResponseRedirect('/puppet_c_s/')
        else:
          form = puppet_admin_modForm()

        return render_to_response('puppet_admin.html', {'form': form},context_instance=RequestContext(request))

'''
定义 应用到主机和是主机租的视图
'''
def puppet_m_app_1(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_mod_host
        show_lines = autopag(request,mod)
        return  render_to_response('puppet_m_app_1.html',{'show_lines':show_lines},context_instance=RequestContext(request))
def puppet_m_app_2(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_mod_group
        show_lines = autopag(request,mod)
        return  render_to_response('puppet_m_app_2.html',{'show_lines':show_lines},context_instance=RequestContext(request))



def puppet_m_app_h(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:

        if request.method == 'POST':
            form = puppet_mod_hostForm(request.POST)
            form1 = puppet_mod_hostForm_h(request.POST)
            id_list = request.POST.getlist('choices')
            id_list_host = request.POST.getlist('choices_host')
            csrf_token = get_token(request)
            for name in id_list:
                for host in id_list_host:
                    ipv4 = puppet_host.objects.filter(name=host).values_list('ip',flat=True)

                    group_name = puppet_host.objects.filter(name=host).values_list('group_name',flat=True)
                    model_active_host(request,name,host)
                    for ip in ipv4:
                      re = puppet_mod_host.objects.filter(mod_name=name,mod_host=host)
                      if not re:
                         #group_name_list = [ group_name.encode("utf8") for group_name in puppet_host.objects.filter(ip=ip).values_list('host_group',flat=True)]
                         group_name = puppet_host.objects.filter(ip=ip).values_list('group_name',flat=True)
                         g_name = json.dumps(list(group_name), cls=DjangoJSONEncoder)
                         g = g_name[2:-2]

                         obj = puppet_mod_host(mod_name=name,mod_host=host,ip=ip,group_name=g)
                         obj.save()
                      else:
                          pass

                      re1 = puppet_mod_group.objects.filter(mod_name=name,mod_group=group_name)
                      if not re1:

                         obj1 = puppet_mod_group(mod_name=name,mod_group=g)
                         obj1.save()

                      else:
                         pass

            return HttpResponseRedirect ('/puppet_m_app_1/')

        else:
              form = puppet_mod_hostForm()
              form1 = puppet_mod_hostForm_h()

        return  render_to_response('puppet_m_app_h.html',{'form': form,'form1': form1 },context_instance=RequestContext(request))
def puppet_m_app_g(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        if request.method == 'POST':
            form = puppet_mod_groupFrom(request.POST)
            form1 = puppet_mod_groupForm_g(request.POST)
            hostgroup = request.POST.getlist('choices')
            mod_name = request.POST.getlist('choices_mod')
            csrf_token = get_token(request)
            for name in mod_name:
                    [group for group in hostgroup]
                    group_id_tmp=Choices_host_group.objects.filter(group_name=group).values_list('id',flat=True)
                    [group_id for group_id in group_id_tmp ]
                    print "ccccc %s ssss %s" %(group_id,group)
                #for group in hostgroup:
                    model_active_group(name,group_id,group)
                    re = puppet_mod_group.objects.filter(mod_name=name,mod_group=group_id)
                    if not re:
                       obj = puppet_mod_group(mod_name=name,mod_group=group)
                       obj.save()
                    else:
                        pass
            return HttpResponseRedirect('/puppet_m_app_2/')
        else:
            form = puppet_mod_groupFrom()
            form1 = puppet_mod_groupForm_g()

        return  render_to_response('puppet_m_app_g.html',{'form':form,'form1':form1 },context_instance=RequestContext(request))


#@login_required
def puppet_admin_c_s(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_admin
        show_lines = autopag(request,mod)
        return render_to_response('puppet_c_s.html', RequestContext(request, {'blog': show_lines,}))


def salt_master_list(request):
     if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
     else:
        mod = salt_admin
        show_lines = autopag(request,mod)
        return render_to_response('salt_master_list.html', RequestContext(request, {'salt_admin': show_lines,}))
@csrf_protect

def salt_master_add(request):
      if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
      else:

          form=salt_adminmodForm(request.POST)

          if request.method=="POST":

            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("salt_master_list"))
          return render_to_response('salt_master_add.html', {'salt_form': form},context_instance=RequestContext(request))

def salt_admin_list(request):
     if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
     else:
        mod = salt_admin
        show_lines = autopag(request,mod)
        return render_to_response('salt_master_list.html', RequestContext(request, {'salt_admin': show_lines,}))

def salt_master_update(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        salt_update=get_object_or_404(salt_admin,pk=int(id))
        if request.method=="POST":
            form=salt_adminmodForm(request.POST,instance=salt_update)
            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("salt_master_list"))
        return render_to_response('salt_master_add.html', {'salt_form': salt_adminmodForm(instance=salt_update)},context_instance=RequestContext(request))

def salt_master_delete (request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        salt=get_object_or_404(salt_admin,pk=int(id))
        salt.delete()
        return HttpResponseRedirect(reverse("salt_master_list"))
'''
def puppet host  group
'''
def host_group(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = Choices_host_group
        show_lines = autopag(request,mod)
        return render_to_response('host_group.html', RequestContext(request, {'show_lines': show_lines,}))

def host_group_add(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        if request.method == 'POST':
           host_group_form = host_group_addForm(request.POST)
           hostgroup_to_idc_local = hostgroup_to_idc_local_Form(request.POST)
           hostgroup_post = request.POST.getlist('choices')

           if host_group_form.is_valid():
                csrf_token = get_token(request)
                group_name = host_group_form.cleaned_data['group_name']
                ip = host_group_form.cleaned_data['ip']
                re = Choices_host_group.objects.filter(group_name=group_name)
                if not re:
                   obj = Choices_host_group(group_name=group_name,ip=ip)
                   obj.save()
                return HttpResponseRedirect('/host_group')
        else:
            host_group_form = host_group_addForm(initial={'ip':'0.0.0.0'})
            hostgroup_to_idc_local = hostgroup_to_idc_local_Form()
        return render_to_response('host_group_add.html', {'host_group_add': host_group_form,'hostgroup_to_idc_local':hostgroup_to_idc_local },context_instance=RequestContext(request))

def host_group_del(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
    ##autopay default 10 lines
        mod = Choices_host_group
        show_lines = autopag(request,mod)
        items = Choices_host_group.objects.all()
        ###get  checkbox id delete
        if request.method == 'POST':
            csrf_token = get_token(request)
            id_list = request.POST.getlist('checkbox')
            if not id_list :
                return render_to_response('error.html',{'id':id_list})
            else:

                int_id_list = [int(id) for id in id_list]  # convert to int
                for id in int_id_list :
                   Choices_host_group.objects.get(id=id).delete()
                return HttpResponseRedirect('/host_group/')

        return render_to_response("host_g_d.html",{'items': items,'show_lines': show_lines,},context_instance=RequestContext(request),)

'''
查看主机状态
'''
def host_list(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_host
        show_lines = autopag(request,mod)
        return render_to_response('host_list.html', RequestContext(request, {'show_lines': show_lines,}))
def host_add(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
          form=host_addForm(request.POST)

          if request.method=="POST":

            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("host_list"))
          return render_to_response('host_add.html', {'form': form},context_instance=RequestContext(request))
def host_update(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        puppet_host_update=get_object_or_404(puppet_host,pk=int(id))
        if request.method=="POST":
            form=host_addForm(request.POST,instance=puppet_host_update)
            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("host_list"))
        return render_to_response('host_add.html', {'form': host_addForm(instance=puppet_host_update)},context_instance=RequestContext(request))

def host_delete(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        host_id=get_object_or_404(puppet_host,pk=int(id))
        hostname=puppet_host.objects.filter(id=id).values_list('name',flat=True)
        [host_name for host_name in hostname]
        res =host_del(host_name)
        if res  == 1:
            print (host_name)
            host_id.delete()
        else:
            print "delete %s failde" %(host_name)

        return HttpResponseRedirect(reverse("host_list"))


def puppet_mod_note_d(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_mod_host
        show_lines = autopag(request,mod)
        items = puppet_mod_host.objects.all()
        ###get  checkbox id delete
        if request.method == 'POST':
            csrf_token = get_token(request)
            id_list = request.POST.getlist('checkbox')
            if not id_list :
                return render_to_response('error.html',{'id':id_list})
            else:

                int_id_list = [int(id) for id in id_list]  # convert to int
                for id in int_id_list :
                    mod_name=puppet_mod_host.objects.filter(id=id).values_list('mod_name',flat=True)
                    mod_host=puppet_mod_host.objects.filter(id=id).values_list('mod_host',flat=True)
                    for modname in mod_name:
                       for hostname in mod_host:
                          if mod_disable_host(modname,hostname) == 1:
                              messages.error(request, '模块没有被删除')
                              #return HttpResponseRedirect('/puppet_mod_note_d/')
                          else:
                              puppet_mod_host.objects.get(id=id).delete()
                              '''
                              检查关联主机组中是否还有其他主机，如果没有，则删除
                              '''
                    l_ = puppet_mod_host.objects.filter(mod_name=mod_name)

                    if  l_:
                                    pass
                    else:
                                   try:
                                        puppet_mod_group.objects.get(mod_name=modname).delete()
                                   except ObjectDoesNotExist:
                                        print 'Does Not Exist!'
                                   except MultipleObjectsReturned:
                                         print 'Does Not Exist!'

                #mod_disable_host()
                return HttpResponseRedirect('/puppet_mod_note_d/')
        return  render_to_response('puppet_mod_note_d.html',{'items':items,'show_lines':show_lines},context_instance=RequestContext(request))


def puppet_mod_file_list(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = puppet_mod_file_upload
        show_lines = autopag(request,mod)
        return render_to_response('puppet_mod_file_list.html', RequestContext(request, {'show_lines': show_lines,}))

from models import salt_main,salt_run_command

def salt_app_g(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        from forms import salt_mainForm,salt_run_commandForm
        form = salt_mainForm()
        from1 = salt_run_commandForm()
        if request.method == 'POST':
            salt_host = request.POST.get('name')
            run_command =  request.POST.get('command')
            host_group_name = request.POST.getlist('host_group')
            try:
                if os.path.isfile('/usr/local/bin/fab'):
                    fab_path = '/usr/local/bin/fab'
                else:
                    messages.error(request,"plaese install fabric ")
                if salt_host is None :

                    messages.error(request,"请选择主机组")

                for h_g_n in host_group_name:

                    host_name = puppet_host.objects.filter(host_group=h_g_n,status='on').values_list('name',flat=True)

                s_h_ip = salt_admin.objects.filter(id=salt_host).values_list('ip',flat=True)

                file_path=os.getcwd()+'/puppet_web_admin/ssh.py'

                for salt_h in s_h_ip:
                        #r = ping(salt_h)
                        res = check_aliveness(salt_h,22)
                        if res == 1:
                                user='root'
                                #pw='puppet_web'
                                for h_name_tmp in host_name:

                                            h_name = h_name_tmp
                                            var_list = ['salt',h_name,'cmd.run']
                                            cmd= ' '.join (str(d) for d in var_list)+ ' \'%s\'' %(run_command)
                                            print (cmd)
                                            cmd1= "%s -f %s -H %s --user=\'%s\'  -t 15 run_shell_command:\"%s\"" %(fab_path,file_path,salt_h,user,cmd)
                                            proc = os.system(cmd1)
                                            ###out print os.system values
                                            ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
                                            fpath = ftmp.name
                                            if os.name=="nt":
                                                fpath = fpath.replace("/","\\") # forwin
                                            ftmp.close()
                                            os.system(cmd1 + " >> " + fpath)
                                            data = ""
                                            with open(fpath, 'r') as file:
                                                data = file.read()
                                                file.close()
                                            os.remove(fpath)
                                            # re_list=re.search("'time out'|error|Fatal|'Timed out'|'Not connected'|Minion|not|Not",data)
                                            # if re_list  is not None :
                                            re_list=re.search('No command was sent',data)
                                            re_list1=re.search('Not connected',data)
                                            re_list2=re.search('error',data)
                                            re_list3=re.search('Fatal',data)
                                            re_list4=re.search('Timed out',data)
                                            re_list5=re.search('Minion',data)
                                            if re_list is not None or re_list1 is not None or re_list2 is not None or re_list3 is not None or re_list4 is not None or re_list5 is not None:

                                                re_l = h_name+'\t'+cmd+'\t run  Faild'

                                            ###inster  to db
                                                ob = salt_run_command(command=re_l,run_user='admin')
                                                ob.save()
                                            else:
                                                print "ok ok ok ok ok %s" %data
                                                re_l=h_name+'\t'+cmd+'\t  run OK'
                                                ob = salt_run_command(command=re_l,run_user='admin')
                                                ob.save()
                        else:

                                re_l= salt_h+'\t saltstack Master connect time out'
                                ob = salt_run_command(command=re_l,run_user='admin')
                                ob.save()
                return  HttpResponseRedirect('/salt_re_list/')
            except:
                print "error"



        return render_to_response('salt_app_g.html',{'form':form,'form1':from1},context_instance=RequestContext(request))

def salt_app_h(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        from forms import salt_mainForm,salt_run_command_h_Form
        form = salt_mainForm()
        form1 = salt_run_command_h_Form()
        if request.method == 'POST':
            salt_host = request.POST.get('name')
            run_command =  request.POST.get('command')
            host_name = request.POST.getlist('host_name')
            try:
                if os.path.isfile('/usr/local/bin/fab'):
                    fab_path = '/usr/local/bin/fab'
                else:
                    messages.error(request,"plaese install fabric ")
                if salt_host is None :
                     messages.error(request,"请选择主机")

                s_h_ip = salt_admin.objects.filter(id=salt_host).values_list('ip',flat=True)
                file_path=os.getcwd()+'/puppet_web_admin/ssh.py'
                [salt_h for salt_h in s_h_ip]
                [h_n for h_n in host_name]
                user='root'
                #pw='puppet_web'
                #for h_name_tmp in host_name:

                res =check_aliveness(salt_h,22)

                if res == 1:
                                        #h_name = h_name_tmp
                                        var_list = ['salt',h_n,'cmd.run']
                                        cmd= ' '.join (str(d) for d in var_list)+ ' \'%s\'' %(run_command)

                                        cmd1= "%s -f %s -H %s --user=\'%s\'  -t 15 run_shell_command:\"%s\"" %(fab_path,file_path,salt_h,user,cmd)
                                        proc = os.system(cmd1)
                                        ###out print os.system values
                                        ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
                                        fpath = ftmp.name
                                        if os.name=="nt":
                                                fpath = fpath.replace("/","\\") # forwin
                                        ftmp.close()
                                        os.system(cmd1 + " >> " + fpath)
                                        data = ""
                                        with open(fpath, 'r') as file:
                                            data = file.read()
                                            file.close()
                                        os.remove(fpath)

                                        re_list=re.search('No command was sent',data)
                                        re_list1=re.search('Not connected',data)
                                        re_list2=re.search('error',data)
                                        re_list3=re.search('Fatal',data)
                                        re_list4=re.search('Timed out',data)
                                        re_list5=re.search('Minion',data)
                                        if re_list is not None or re_list1 is not None or re_list2 is not None or re_list3 is not None or re_list4 is not None or re_list5 is not None:

                                                re_l = h_n+'\t'+cmd+'\t run  Faild'
                                                ob = salt_run_command(command=re_l,run_user='admin')
                                                ob.save()
                                        else:

                                                re_l=h_n+'\t'+cmd+'\t  run ok'
                                                ob = salt_run_command(command=re_l,run_user='admin')
                                                ob.save()
                                        print (re_list)
                else:

                                        re_l= salt_h+'\t saltstack Master connect time out'
                                        ob = salt_run_command(command=re_l,run_user='admin')
                                        ob.save()
                return  HttpResponseRedirect(reverse('salt_re_list'))

            except:
                 print "error"

        return  render_to_response('salt_app_h.html',{'form':form,'form1':form1},context_instance=RequestContext(request))

def salt_re_list(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = salt_run_command
        show_lines = autopag(request,mod)
        return render_to_response('salt_re_list.html', RequestContext(request, {'show_lines': show_lines,}))

'''
idc
'''
def idc_list(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        mod = idc
        show_lines = autopag(request,mod)
        return render_to_response('idc_list.html', RequestContext(request, {'show_lines': show_lines,}))

def idc_add(request):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
          form=idcForm(request.POST)

          if request.method=="POST":

            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("idc_list"))
          return render_to_response('idc_add.html', {'form': form},context_instance=RequestContext(request))
def idc_update(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        puppet_host_update=get_object_or_404(puppet_host,pk=int(id))
        if request.method=="POST":
            form=host_addForm(request.POST,instance=puppet_host_update)
            if form.is_valid():
                csrf_token = get_token(request)
                form.save()

                return HttpResponseRedirect(reverse("host_list"))
        return render_to_response('host_add.html', {'form': host_addForm(instance=puppet_host_update)},context_instance=RequestContext(request))

def idc_delete(request,id):
    if not request.user.is_authenticated():
         return HttpResponseRedirect(reverse('root'))
    else:
        host_id=get_object_or_404(puppet_host,pk=int(id))
        hostname=puppet_host.objects.filter(id=id).values_list('name',flat=True)
        [host_name for host_name in hostname]
        res =host_del(host_name)
        if res  == 1:
            print (host_name)
            host_id.delete()
        else:
            print "delete %s failde" %(host_name)

        return HttpResponseRedirect(reverse("host_list"))



