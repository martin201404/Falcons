#-*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os,sys,re,chunk,shutil,socket
from puppet_web.models import puppet_mod_file_upload,puppet_admin,puppet_host,salt_admin,puppet_edit_config,Choices_host_group,puppet_mod_group,puppet_mod_host

###autopay
def autopag(request,mod):
    lines = mod.objects.all().order_by('-id')
    paginator = Paginator(lines,10000000)
    page = request.GET.get('page')
    try:
           show_lines = paginator.page(page)
    except PageNotAnInteger:
        #    # If page is not an integer, deliver first page.
           show_lines = paginator.page(1)
    except EmptyPage:
        #    # If page is out of range (e.g. 9999), deliver last page of results.
           show_lines = paginator.page(paginator.num_pages)
    return show_lines

def fun_findstr(filepath,findstr):
  if os.path.isfile(filepath):
    thefile=open(filepath, 'rb')
    while True:
        buffer = thefile.read(104857600)
        if not buffer:
            break
        for match in re.findall('\n.*'+findstr+'.*\n',buffer):
            return 1


    thefile.close()


def byte_string(x):
    return str(x) if isinstance(x, unicode) else x



from fabric.contrib.files import *
from fabric.api import *
from fabric.colors import *
from fabric.tasks import *

def shell_run_command(requst,ip,port,username,password,cmd):
    env.hosts = ip
    env.port = port
    env.user = username
    env.password = password
    run('ls /tmp')
    #return re

def ping(host):
    response = os.system("ping -c 3 " + host)
    if response == 0:
        return 0
    else:
        return 1

def check_aliveness(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(5)
    try:
        sk.connect((ip,port))
        print 'saltmaster ssh check  %s %d satus is OK!' %(ip,port)
        return 1
    except Exception:
        print 'saltmaster ssh  server %s %d connect faild,please check ssh  server config!'  %(ip,port)
        return 0
    finally:
        sk.close()
    return 0