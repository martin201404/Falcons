
#-*- coding: utf-8 -*-
from django.db import models,connection
from django import forms
from django.contrib import admin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class idc (models.Model):
    idc_name = models.CharField(u'idc name',max_length=200,null=True)
    idc_floor = models.CharField(u'楼层',max_length=10,null=True)
    idc_cabinets = models.CharField(u'机柜',max_length=10,null=True)


    def __unicode__(self):
        return  self.idc_name

class puppet_admin(models.Model):

    puppet_model_path = models.CharField(u'puppet模块路径',max_length= 100,null=True)
    puppet_files_server_path =models.CharField(u'配置文件服务器',max_length=100,null=True)
    puppet_config_path = models.CharField(u'puppet 配置文件',max_length=200,null=True)
    puppet_server_ip = models.CharField(u'puppet ip',max_length=50,null=True)
    def __unicode__(self):
        return self.puppet_model_path + ' ' + self.puppet_files_server_path + ' ' + self.puppet_config_path +' '+ self.puppet_server_ip
    class Meta:
        ordering = ['id']

'''
定义puppet 主机
'''
class puppet_host(models.Model):
    GENDER_CHOICES = (
        ('on', 'on'),
        ('off', 'off'),
    )
    OS_CHOICES = (
        ('Centos', 'Centos'),
        ('FreeBSD', 'FreeBSD'),
        ('RedHat','RedHat'),
        ('Debian','Debian'),
        ('Ubuntu','Ubuntu'),
        ('Gentoo','Gentoo'),
        ('OpenSUSE','OpenSUSE'),
    )
    ip = models.GenericIPAddressField(u'ip 地址',blank=True,null=True)
    name = models.CharField(u'主机名',max_length=200,null=True)
    status = models.CharField(u'主机状态',max_length=3, choices=GENDER_CHOICES)
    os_varsion = models.CharField(u'操作系统',max_length=10,choices=OS_CHOICES)
    idc_name = models.ForeignKey('idc',null=True,blank=True)
    idc_floor = models.CharField(u'楼层',max_length=4,null=True,blank=True)
    idc_cabinets = models.CharField(u'机柜号',max_length=10,null=True,blank=True)
    #host_group = models.CharField(u'主机组',max_length=100,null=True)
    group_name = models.ForeignKey('Choices_host_group',null=True, blank=True,related_name='group_name_group_name')
    salt_name = models.ForeignKey('salt_admin',null=True,blank=True)

    def __unicode__(self):

        return self.ip + ' ' + self.name + ' ' + self.status + ' ' + self.os_varsion
'''
定义 puppet 主机应用到组，模块的数据结构
'''
class puppet_mod_host(models.Model):
    mod_name = models.CharField(u'模块名',max_length=100,null=True)
    mod_host = models.CharField(u'主机名',max_length=200,null=True)
    ip = models.GenericIPAddressField(u'ipv4',blank=True,null=True)
    group_name = models.CharField(u'主机组',max_length=50,null=True)
    def __unicode__(self):
        return self.mod_host

class puppet_mod_group(models.Model):
    mod_name = models.CharField(u'模块名',max_length=100,null=True)
    mod_group = models.CharField(u'主机组',max_length=200,null=True)

    def __unicode__(self):
        return  self.mod_g_name





'''
定义主机组
'''
'''
class Choices_host_groupManager(models.Manager):
    group_name = [ ]
    def group_name(self,group_name):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT DISTINCT group_name
        FROM register_Choices_host_group
        where id in (%s) """, [group_name])
        return cursor.fetchall()
'''
class Choices_host_group(models.Model):

  group_name = models.CharField(u'组名',max_length=300,null=True)
  ip = models.GenericIPAddressField(u'主机ip',blank=True,null=True)
  idc = models.CharField(u'idc',max_length=200,null=True)
  role_name=models.ForeignKey('role',blank=True,null=True)
  #objects = Choices_host_groupManager()

  def __unicode__(self):
     #return  self.group_name
     return u'%s'%(self.group_name)


'''
定义puppet 模块关系
'''
class puppet_edit_config(models.Model):


    model_name = models.CharField(u'模块名字',max_length=50,null=True)
    file_name = models.CharField(u'文件名',max_length=20,null=True)
    contents = models.TextField(u'内容',max_length=10000000,null=True,editable=True,blank=True,)
    def __unicode__(self):

        return  self.model_name

class puppet_models(models.Model):

    model_name = models.CharField(u'model name',max_length=200,null=True)
    def __unicode__(self):
        #return u'%s' % (self.model_name)
        return  self.model_name


class puppet_mod_file_upload(models.Model):
   model_name = models.CharField(u'模块名',max_length=50,null=True)
   file = models.FileField()
   describe = models.TextField(u'备注',null=True,max_length=200)
   def __str__(self):
       return "(%s) %s" % (self.model_name)
   def __unicode__(self):
       return self.model_name

'''
salt
'''

class salt_admin(models.Model):

    ip = models.GenericIPAddressField(u'salt master ip',blank=True,null=True)
    salt_name = models.CharField(u'salt master 主机名',max_length=50,null=True)
    local = models.CharField(u'salt master 位置',max_length=200,null=True)

    def __unicode__(self):

        return self.salt_name

class salt_main(models.Model):

    salt_name = models.ForeignKey(salt_admin)


class salt_run_command(models.Model):

    command = models.CharField(u'command',max_length=1500,null=True)
    run_time = models.DateTimeField(u'运行时间 ',auto_now=True)
    run_user = models.CharField(u'用户',max_length=40,null=True)

    def __unicode__(self):
        return self.command


'''
user manager
'''
class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    group_name= models.ManyToManyField(Choices_host_group,null=True,blank=True)

    def __unicode__(self):
        return '%s(%s) %s' %(self.name,self.hostname,self.group_name)


class RoleList(models.Model):
    name = models.CharField(max_length=64)
    group_name = models.ManyToManyField(PermissionList,null=True,blank=True)

    def __unicode__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(email,
            username = username,
            password = password,
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class role(models.Model):

    role_name=models.CharField(u'角色名称',max_length=30,null=True)
    user_group=models.CharField(u'用户组',max_length=30,null=True)
    role_status=models.CharField(max_length=5,null=True)
    def __unicode__(self):
       return self.role_name
class User_group(models.Model):

    user_group = models.CharField(u'用户组',max_length=40,null=True)
    #username =models.ForeignKey(User,null=True,blank=True)

    def __unicode__(self):
        return  self.user_group

class User(AbstractBaseUser):

    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    sex = models.CharField(max_length=2, null=True)
    user_group = models.ForeignKey(User_group,null=True,blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self,perm,obj=None):
        if self.is_active and self.is_superuser:
            return True
    def __unicode__(self):

        return unicode(self.username)




class role_to_host(models.Model):

    role_name_id = models.PositiveIntegerField(null=True)
    host_id=models.PositiveIntegerField(null=True)

class usergroup_to_model(models.Model):
    user_group_id = models.PositiveIntegerField(null=True)
    model_id = models.PositiveIntegerField(null=True)
