#coding: utf-8
from django import forms
from django.forms import ModelForm
from models import puppet_mod_file_upload,puppet_admin,salt_admin,puppet_edit_config,Choices_host_group,puppet_host,puppet_mod_host,puppet_mod_group,idc,User,PermissionList,RoleList,User_group
from checkboxselectmultiple.widgets import CheckboxSelectMultiple

class idcForm(ModelForm):
    class Meta:
        model = idc
        fields = '__all__'

class UserFrom(forms.Form):
    usernmae = forms.CharField(
        label='用户名'
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
    )


class puppet_from(forms.Form):
      puppet_model_path = forms.CharField(
          label='puppet 模块路径',

      )
      puppet_files_server_path = forms.CharField(
          label='puppet 文件服务器配置文件',

      )
      puppet_config_path = forms.CharField(
          label='puppet 配置文件路径',

      )
      puppet_server_ip = forms.CharField(
          label='puppet 主机名'
      )
class puppet_admin_modForm(forms.ModelForm):
    class Meta:
        model = puppet_admin
        fields = '__all__'

        #exclude = ()
    def clean(self):
        cleaned_data = super(puppet_admin_modForm, self).clean()
        puppet_model_path = cleaned_data.get('puppet_model_path')
        puppet_files_server_path = cleaned_data.get('puppet_files_server_path')
        puppet_config_path = cleaned_data.get('puppet_config_path')
        puppet_server_ip = cleaned_data.get('puppet_server_ip')
        if not puppet_server_ip:
            self._errors['puppet_server_ip'] =  self.error_class([u"请输入主机名"])
        if not puppet_config_path:
            self._errors['puppet_config_path'] = self.error_class([u"请输入配置文件路径"])
        if not puppet_files_server_path:
            self._errors['puppet_files_server_path'] = self.error_class([u"请输入文件服务器配置文件路径"])
        if not puppet_model_path:
            self._errors['puppet_model_path'] = self.error_class([u"请输入模块路径"])

'''
add model detail
'''
class puppet_edit_confForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(puppet_edit_confForm, self).clean()
        model_name = cleaned_data.get('model_name')
        file_name = cleaned_data.get('file_name')
        contents = cleaned_data.get('contents')
        if not contents:
            self.errors['contents'] = self.error_class([u"文件内容不能为空"])
        if not model_name:
            self.errors['model_name'] = self.error_class([u"模块名称不能为空"])
        if not file_name:
            self.errors['file_name'] = self.error_class([u"文件名不能为空"])
    class Meta:
        model = puppet_edit_config
        fields = '__all__'
        widgets = {
          'contents': forms.Textarea(attrs={
                                  'style': 'height: 200px;width:500px'}),
        }
        exclude = ['host_group']
'''
update model detail
'''
class puppet_edit_update(ModelForm):
    class Meta:
        model=puppet_edit_config
        #exclude=[]
        fields='__all__'

class puppet_mod_file_uploadForm(forms.ModelForm):

    choices_model_name = forms.ModelMultipleChoiceField(queryset=puppet_edit_config.objects.all().values_list('model_name',flat=True).distinct(),required=False,widget=forms.RadioSelect)
    class Meta:
        model = puppet_mod_file_upload
        #fields = '__all__'
        exclude=['file_path','model_name']

class Choices_host_groupForm(forms.ModelForm):
    the_choices = forms.ModelMultipleChoiceField(queryset=Choices_host_group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Choices_host_group
        #fields = '__all__'
        exclude = ['group_ip']

class host_group_addForm(forms.ModelForm):

    class Meta:
        model = Choices_host_group
        #fields = '__all__'
        exclude = ['idc']

class puppet_form(forms.Form):
    ip = forms.CharField(
        label='salt master ip'
    )
    name = forms.CharField(
        label='salt master name'
    )

class puppet_mod_hostForm(forms.ModelForm):

    choices = forms.ModelMultipleChoiceField(queryset=puppet_edit_config.objects.values_list('model_name',flat=True).distinct(),required=False,widget=forms.CheckboxSelectMultiple)


    def clean(self):
        cleaned_data = super(puppet_mod_hostForm, self).clean()
        mod_name = cleaned_data.get('mod_name')
        mod_host = cleaned_data.get('mod_host')
        if not mod_host :
            self.errors['mod_host'] = self.error_class([u"主机名不能为空"])
        if not mod_name:
            self.errors['mod_name'] = self.error_class([u"模块名不能为空"])
    class Meta:
        model = puppet_mod_host
        #css = {
        #   'all': 'puppet_web_admin/checkbox.css',
        #}
        #fields = '__all__'
        exclude = ['mod_host','mod_name','ip','group_name']
    def __unicode__(self):
        return self.name
class puppet_mod_hostForm_h(forms.ModelForm):

    choices_host = forms.ModelMultipleChoiceField(queryset=puppet_host.objects.filter(status='on').values_list('name',flat=True),required=False,widget=forms.CheckboxSelectMultiple)
    def clean(self):
        cleaned_data = super(puppet_mod_hostForm_h, self).clean()
        mod_name = cleaned_data.get('mod_name')
        mod_group = cleaned_data.get('mod_group')
        if not mod_name:
            self.errors['mod_name'] = self.error_class(u"模块名不能为空")
        if not mod_group:
            self.errors['mod_group'] = self.error_class(u"主机组不能为空")

    class Meta:
        model = puppet_host
        #fields = '__all__'
        salt_master ={

        }
        exclude = ['ip','status','os_varsion','name','idc_cabinets','idc_floor','idc_name','group_name','salt_name']

class puppet_mod_groupFrom(forms.ModelForm):

    choices = forms.ModelMultipleChoiceField(queryset=Choices_host_group.objects.values_list('group_name',flat=True),required=False,widget=forms.CheckboxSelectMultiple)

    def clean_mod_group(self):
        mod_group = self.cleaned_data('mod_group')
        num_words=len(mod_group.split())
        if num_words < 1:
            raise forms.ValidationError("Not")
        return mod_group

    class Meta:

        model = puppet_mod_group
        #fields = '__all__'
        exclude = ['mod_name','mod_group']


class puppet_mod_groupForm_g(forms.ModelForm):
     choices_mod = forms.ModelMultipleChoiceField(queryset=puppet_edit_config.objects.values_list('model_name',flat=True).distinct(),required=False,widget=forms.CheckboxSelectMultiple)

     class Meta:
         model = puppet_edit_config
         exclude = ['model_name','file_name','contents','group_name']

'''
idc 与 主机组的对应关系
'''
class hostgroup_to_idc_local_Form(forms.ModelForm):
    choices = forms.ModelMultipleChoiceField(queryset=idc.objects.values_list('idc_name',flat=True),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
         model = idc
         exclude = ['floor','cabinets','name']


'''
salt
'''

class salt_adminmodForm(forms.ModelForm):

    class Meta:
        model = salt_admin
        fields = '__all__'
class salt_master_addForm(ModelForm):
    class Meta:
        model= salt_admin
        fields ='__all__'

from models import salt_main
class salt_mainForm(forms.ModelForm):

    class Meta:
       model = salt_main
       exclude =['']

from models import salt_run_command
class salt_run_commandForm(forms.ModelForm):
    res=puppet_host.objects.filter(status='on').values_list('group_name',flat=True).distinct()
    #for res1 in res:
    host_group = forms.ModelMultipleChoiceField(queryset=puppet_host.objects.filter(status='on').values_list('group_name',flat=True).distinct(),required=False,widget=forms.RadioSelect)
    class Meta:
        model = salt_run_command
        exclude = ['run_user']

class salt_run_command_h_Form(forms.ModelForm):
    host_name = forms.ModelMultipleChoiceField(queryset=puppet_host.objects.filter(status='on').values_list('name',flat=True).distinct(),required=False,widget=forms.RadioSelect)
    class Meta:
        model = salt_run_command
        exclude = ['run_user']

'''
host status
'''
class host_addForm(ModelForm):
    #user_group= forms.ModelMultipleChoiceField(queryset=User_group.objects.values_list('user_group',flat=True).distinct(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = puppet_host
        exclude = []
    def __init__(self,*args,**kwargs):
        super(host_addForm, self).__init__(*args,**kwargs)
        self.fields['group_name'].label=u'选择主机组'
        self.fields['salt_name'].label=u'选择salt master'
'''
user manager
'''
from django.contrib import auth
class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,password=password)
            print (self.user_cache)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配,请检查或者联系管理员')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原始密码',error_messages={'required':'请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label=u'新密码',error_messages={'required':'请输入新密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=u'重复输入',error_messages={'required':'请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email','nickname','sex','user_group','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'nickname' : forms.TextInput(attrs={'class':'form-control'}),
            'sex' : forms.RadioSelect(choices=((u'男', u'男'),(u'女', u'女')),attrs={'class':'list-inline'}),
            'user_group' : forms.Select(attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(AddUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['password'].label=u'密 码'
        self.fields['password'].error_messages={'required':u'请输入密码'}
        self.fields['email'].label=u'邮 箱'
        self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        self.fields['nickname'].label=u'姓 名'
        self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        self.fields['sex'].label=u'性 别'
        self.fields['sex'].error_messages={'required':u'请选择性别'}
        self.fields['user_group'].label=u'用户组'
        self.fields['is_active'].label=u'状 态'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(u'密码必须大于6位')
        return password

#from models import User_group
class AddUserGroupForm(forms.ModelForm):
    class Meta:
        model = User_group
        fields='__all__'

'''
'''
class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        fields ='__all__'
    def __init__(self):
        super(PermissionListForm, self).__init__()
        self.fields['name'].label=u'名称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['group_name'].label=u'主机组'

class PermissionAddForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        exclude = ['hostname']
        #fields ='__all__'


from models import role

class RoleListForm(forms.ModelForm):

    user_group = forms.ModelMultipleChoiceField(queryset=User_group.objects.all().values_list('user_group',flat=True).distinct(),required=False,widget=forms.RadioSelect)
    class Meta:
        model = PermissionList
        fields ='__all__'
        #exclude = ['user_group']



class RoleForm(forms.ModelForm):

    user_group = forms.ModelMultipleChoiceField(queryset=User_group.objects.all().values_list('user_group',flat=True).distinct(),required=False,widget=forms.CheckboxSelectMultiple)
    host_name = forms.ModelMultipleChoiceField(queryset=puppet_host.objects.filter(status='on').values_list('name',flat=True).distinct(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = role
        #exclude = ['user_group','role_status']
        fields = ('role_name','role_status')
        widgets = {
            'role_name' : forms.TextInput(attrs={'class':'form-control'}),
            'role_status' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

    class Media:
        js = ['admin/js/jquery-ui-1.10.2.custom.js', 'admin/js/checkboxselectmultiple.css']
        css = {
            'all': ('admin/css/jquery-ui-1.10.2.custom.css', 'admin/css/checkboxselectmultiple.css',)
        }
    def __init__(self,*args,**kwargs):
          super(RoleForm, self).__init__(*args,**kwargs)
    #       self.fields['user_group'].choices= [(e.id,e.user_group) for e in User_group.objects.all().distinct()]
    #
          self.fields['user_group'].label=u'选择用户组'
          self.fields['user_group'].error_messages={'required':u'请选择用户组'}
          self.fields['role_status'].label=u'角色状态'
          self.fields['host_name'].label=u'请选择主机'


