# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
from django.utils.translation import ugettext_lazy as _, ugettext
import re
from django import forms
from django.conf import settings
from TripleMag.apps.money.models import cash_withdraw,cash_trans
from TripleMag.apps.member.models import user_basic


from django.forms import ModelForm
from TripleMag.apps.views import verify_password_2nd
class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)

class WithdrawForm(ModelForm):
    #用户体现登表单
    password_2nd = forms.CharField(
        label = _("二级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    class Meta:
        model = cash_withdraw
        exclude = ("user",'state','time')
        
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)
        super(WithdrawForm, self).__init__(*args, **kwargs)
    
    def clean_password_2nd(self):

        password_2nd = self.cleaned_data['password_2nd']
        
        verify_result = verify_password_2nd(password_2nd,self.user)
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd
        
class CashTransForm(ModelForm):
    #互转表
    user_to = forms.CharField(
        label = _("目标编号"),
        widget = forms.TextInput(),
        max_length = 8,
        required = True
    )
    password_2nd = forms.CharField(
        label = _("二级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)
        print self.user,'fffffffffff'
        super(CashTransForm, self).__init__(*args, **kwargs)
    class Meta:
        exclude = ("user_from","user_to")
        model = cash_trans

    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        verify_result = verify_password_2nd(password_2nd,self.user)
        print verify_result,'ssssssssssssss'
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd
        
    def clean_user_to(self):
        user_to = self.cleaned_data['user_to']

        UserBasic = user_basic.objects.defer(None).filter(number = user_to)
        if not UserBasic:
            raise forms.ValidationError("不存在此用户")
        return user_to

        
        
