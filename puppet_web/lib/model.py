#-*- coding: utf-8 -*-
from puppet_web.models import puppet_admin,puppet_host,salt_admin,puppet_edit_config,Choices_host_group,puppet_mod_group,puppet_mod_host,idc
import os,sys,shutil,re
from puppet_web.lib.base import fun_findstr
from django.contrib import messages
from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
import time

def model_new(request,mod_name,files_name,contents):

    puppet_mod_path1=puppet_admin.objects.all().values_list('puppet_model_path',flat=True)
    for puppet_mod_path in puppet_mod_path1:
     if not os.path.exists(puppet_mod_path+'/'+mod_name+'/files'):
       os.makedirs(puppet_mod_path+'/'+mod_name+'/files')
     if not os.path.exists(puppet_mod_path+'/'+mod_name+'/manifests'):
       os.makedirs(puppet_mod_path+'/'+mod_name+'/manifests')
     if not os.path.exists(puppet_mod_path+'/'+mod_name+'/templates'):
       os.makedirs(puppet_mod_path+'/'+mod_name+'/templates')

    f = open('/tmp/files_name',mode='w')
    f.write(contents)
    f.close()
    os.chdir(puppet_mod_path+'/'+mod_name+'/manifests')
    shutil.copyfile('/tmp/files_name',files_name)
    os.remove('/tmp/files_name')
def model_update(request,mod_name,files_name,contents):
    puppet_mod_path1=puppet_admin.objects.all().values_list('puppet_model_path',flat=True)
    [puppet_mod_path for puppet_mod_path in puppet_mod_path1]
    f = open('/tmp/files_name',mode='w')
    f.write(contents)
    f.close()
    os.chdir(puppet_mod_path+'/'+mod_name+'/manifests')
    now = int(time.time())
    t=time.localtime(now)

    o_t=time.strftime("%Y-%m-%d-%H:%M:%S",t)
    os.renames(files_name,files_name+'_'+o_t)
    shutil.copyfile('/tmp/files_name',files_name)
    os.remove('/tmp/files_name')

def model_del(request,mod_name):
    puppet_mod_path1=puppet_admin.objects.all().values_list('puppet_model_path',flat=True)
    for puppet_mod_path in puppet_mod_path1:
      if not os.path.exists(puppet_mod_path+'/'+mod_name):
          pass
      else:
          shutil.rmtree(puppet_mod_path+'/'+mod_name)
          puppet_edit_config.objects.filter(model_name=mod_name).delete()
          puppet_mod_group.objects.filter(mod_name=mod_name).delete()
          puppet_mod_host.objects.filter(mod_name=mod_name).delete()


def model_active_host(request,mod_name,hostname):
    puppet_main_path_tmp = puppet_admin.objects.all().values_list('puppet_config_path',flat=True)
    for puppet_main_path in puppet_main_path_tmp:
        if not os.path.exists(puppet_main_path):
            return 'error'

        else:
          if not os.path.exists(puppet_main_path+'/manifests/nodes'):
             os.makedirs(puppet_main_path+'/manifests/nodes')
          if not os.path.isfile(puppet_main_path+'/manifests/nodes/'+hostname+'.pp'):
            f = open(puppet_main_path+'/manifests/nodes/'+hostname+'.pp',mode='a')
            f.write("node   \'" + hostname  + "\'  inherits  basenode {\n")
            f.write('     include  '+mod_name+'\n')
            f.write('}\n')
            f.close()
          else:
              filepath=puppet_main_path+'/manifests/nodes/'+hostname+'.pp'
              findstr=mod_name
              res = fun_findstr(filepath,findstr)
              if res != 1:

                 fp = file(puppet_main_path+'/manifests/nodes/'+hostname+'.pp')
                 s = fp.read()
                 fp.close()
                 a = s.split('\n')
                 a.insert(1, '      include  '+mod_name ) # 在第二行插入
                 s = '\n'.join(a)
                 fp = file(puppet_main_path+'/manifests/nodes/'+hostname+'.pp', 'w')
                 fp.write(s)
                 fp.close()




    if os.path.isfile(puppet_main_path+'/manifests/init.pp'):
        f = open(puppet_main_path+'/manifests/site.pp',mode='w')
        f.write('Exec { path => "/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/bin:/sbin" } \n')
        f.write('Package { \n')
        f.write('       allow_virtual => true,\n')
        f.write('}\n')

        f.write('node basenode {\n')
        f.write('\n')
        f.write('}\n')
        f.write('import "nodes/*.pp"\n')
        f.close()
    else:
        f = open(puppet_main_path+'/manifests/site.pp',mode='w')
        f.write('Exec { path => "/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/bin:/sbin" }\n')
        f.write('Package {\n')
        f.write('     allow_virtual => true,\n')
        f.write('}\n')
        f.write('node basenode {\n')
        f.write('\n')
        f.write('}\n')
        f.write('import "nodes/*.pp"\n')
        f.close()


def model_active_group(mod_name,host_group,group_name):

    puppet_main_path_tmp = puppet_admin.objects.all().values_list('puppet_config_path',flat=True)
    hostname=puppet_host.objects.filter(group_name=host_group,status='on').values_list('name',flat=True)
    for puppet_main_path in puppet_main_path_tmp:
        if not os.path.exists(puppet_main_path):
            return 'error'

        else:
            if not os.path.exists(puppet_main_path+'/manifests/nodes'):
                os.makedirs(puppet_main_path+'/manifests/nodes')
            for host_name in hostname:
              findstr=mod_name
              filepath=puppet_main_path+'/manifests/nodes/'+host_name+'.pp'
              res = fun_findstr(filepath,findstr)
              if res != 1:
                  if not os.path.isfile(puppet_main_path+'/manifests/nodes/'+host_name+'.pp'):
                    f = open(puppet_main_path+'/manifests/nodes/'+host_name+'.pp',mode='a')
                    f.write("node   \'" + host_name  + "\'  inherits  basenode {\n")
                    f.write('     include  '+mod_name+'\n')
                    f.write('}\n')
                    f.close()
                    ipv4 = puppet_host.objects.filter(name=host_name).values_list('ip',flat=True)
                    for ip in ipv4:
                        re = puppet_mod_host.objects.filter(mod_name=mod_name,mod_host=host_name)
                        if not re:

                            obj = puppet_mod_host(mod_name=mod_name,mod_host=host_name,ip=ip)
                            obj.save()
                  else:
                        fp = file(puppet_main_path+'/manifests/nodes/'+host_name+'.pp')
                        s = fp.read()
                        fp.close()
                        a = s.split('\n')
                        a.insert(1, '      include  '+mod_name ) # 在第二行插入
                        s = '\n'.join(a)
                        fp = file(puppet_main_path+'/manifests/nodes/'+host_name+'.pp', 'w')
                        fp.write(s)
                        fp.close()
                        ipv4 = puppet_host.objects.filter(name=host_name).values_list('ip',flat=True)
                        for ip in ipv4:
                            re = puppet_mod_host.objects.filter(mod_name=mod_name,mod_host=host_name)
                            if not re:
                                obj = puppet_mod_host(mod_name=mod_name,mod_host=host_name,ip=ip,group_name=group_name)
                                obj.save()
    if os.path.isfile(puppet_main_path+'/manifests/init.pp'):
        f = open(puppet_main_path+'/manifests/site.pp',mode='w')
        f.write('Exec { path => "/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/bin:/sbin" } \n')
        f.write('Package { \n')
        f.write('       allow_virtual => true,\n')
        f.write('}\n')
        f.write('node basenode {\n')
        f.write('\n')
        f.write('}\n')
        f.write('import "nodes/*.pp"\n')

        f.close()
    else:
        f = open(puppet_main_path+'/manifests/site.pp',mode='w')
        f.write('Exec { path => "/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/bin:/sbin" }\n')
        f.write('Package {\n')
        f.write('     allow_virtual => true,\n')
        f.write('}\n')
        f.write('node basenode {\n')
        f.write('\n')
        f.write('}\n')
        f.write('import "nodes/*.pp"\n')
        f.close()

def mod_disable_host(mod_name,hostname):
    puppet_config_path1=puppet_admin.objects.all().values_list('puppet_config_path',flat=True)
    for puppet_config_path in puppet_config_path1:
      if not os.path.exists(puppet_config_path):
          return 1
      else:
          if os.path.isfile(puppet_config_path+'/manifests/nodes/'+hostname+'.pp'):
            with open(puppet_config_path+'/manifests/nodes/'+hostname+'.pp', 'r') as f:
              with open('/tmp/'+hostname+'.pp', 'w') as g:
                for line in f.readlines():
                    if mod_name not in line:
                       g.write(line)
            shutil.move('/tmp/'+hostname+'.pp', puppet_config_path+'/manifests/nodes/'+hostname+'.pp')

            #if os.path.getsize(puppet_config_path+'/manifests/nodes/'+hostname+'.pp') < 52:
            count=0
            try:
                handle = open(puppet_config_path+'/manifests/nodes/'+hostname+'.pp','r')
                for eachline in handle:
                    count +=1
                if count < 3:
                      os.remove(puppet_config_path+'/manifests/nodes/'+hostname+'.pp')
                      pass
            except IOError,e:
                print "file open error",e

          else:
              pass
def host_del(hostname):
    puppet_model_path1=puppet_admin.objects.all().values_list('puppet_model_path',flat=True)
    [puppet_model_path for puppet_model_path in puppet_model_path1]
    #for puppet_config_path in puppet_config_path1:
    if not os.path.exists(puppet_model_path+'/../manifests/nodes/'+hostname+'.pp'):
          print "puppet config path %s" %(puppet_model_path)
          return 0
    else:
          os.remove(puppet_model_path+'/../manifests/nodes/'+hostname+'.pp')
          return 1



