# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

import re
from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.exceptions import ValidationError  
from TripleMag.apps.member.models import user_modify_record,message,min_upgrade_record
from TripleMag.apps.views import verify_password_2nd
from tinymce.widgets import TinyMCE


class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)

class MessageForm(forms.Form):
    #用户留言
    content = forms.CharField(widget=forms.Textarea,required=True)


#class VIPApplaction(BasicForm):
#    #商城用户升级VIP申请表    
#    name = forms.CharField(
#        label = _("用户姓名"),
#        max_length=30,
#        widget = forms.TextInput(),
#        required = False
#    )
#    bank_name = forms.CharField(
#        label = _("银行名称"),
#        max_length = 20,
#        widget = forms.TextInput(),
#        required = False
#    )
#    bank_account_name = forms.CharField(
#        label = _("开户人姓名"),
#        max_length = 20,
#        widget = forms.TextInput(),
#        required = False
#    )
#    bank_account_id = forms.CharField(
#        label = _("银行卡号"),
#        max_length = 40,
#        widget = forms.TextInput(),
#        required = False
#    )
    
#class ChangeInfoApplaction(ChangeInfoApplaction):
#    #用户提交修改信息申请 
#    mobile = forms.CharField(
#        label = _("手机号码"),
#        max_length = 13,
#        widget = forms.TextInput(),
#        required =False
#    )
#    id_card_num = forms.CharField(
#        label = _("身份证号"),
#        max_length = 20,
#        widget = forms.TextInput(),
#        required =False
#    )

class ChangeInfo(BasicForm):

    #会员修改信息
    password1 = forms.CharField(
        label = _("一级密码"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True)
    )
    password1_again = forms.CharField(
        label = _("一级密码确认"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True)
    )
    password2 = forms.CharField(
        label = _("二级密码"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True)
    )
    password2_again = forms.CharField(
        label = _("二级密码确认"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True)
    )
    phone = forms.CharField(
        label = _("固定电话"),
        max_length = 20,
        widget = forms.TextInput()
    )
    QQ = forms.CharField(
        label = _("QQ号码"),
        max_length = 20,
        widget = forms.TextInput()
    )
class UpgradeForm(BasicForm):
    remarks = forms.CharField(
        label = _("申请备注"),
        widget = forms.Textarea,
        required = False
    )
    
    
class ChangeInfoApplForm(ModelForm):
    #信息申请表单
    password_2nd = forms.CharField(
        label = _("二级密码"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True),
        required = False
    )    
    
    name = forms.CharField(
        widget = forms.TextInput(),
        required = False
    )
    bank_name = forms.CharField(
        widget = forms.TextInput(),
        required = False
    )
    bank_account_name = forms.CharField(
        widget = forms.TextInput(),
        required = False
    )
    bank_account_id = forms.CharField(
        widget = forms.TextInput(),
        required = False
    )
    id_card_num = forms.CharField(
        widget = forms.TextInput(),
        required = False
    )

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)

        super(ChangeInfoApplForm, self).__init__(*args, **kwargs)
    class Meta:
        model = user_modify_record
        exclude = ('user','state','time')
        
    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        verify_result = verify_password_2nd(password_2nd,self.user)
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd
class MemVipApllForm(ModelForm):
    """
    申请VIP表单
    """
    password_2nd = forms.CharField(
        label = _("二级密码"),
        max_length=200,
        widget = forms.PasswordInput(render_value=True),
        required = True
    )    
    
    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        verify_result = verify_password_2nd(password_2nd,self.user)
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd
    
    class Meta:
        model = min_upgrade_record
        exclude = ('user','state','time')
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)

        super(MemVipApllForm, self).__init__(*args, **kwargs)
    
    
    

        
