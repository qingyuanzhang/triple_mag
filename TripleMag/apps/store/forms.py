# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms import ModelForm

from TripleMag.apps.views import verify_password_2nd
from TripleMag.apps.store.models import stuff_type
from TripleMag.apps.member.models import user_address
class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)

class StoreForm(forms.Form):
    amount = forms.IntegerField(
        label = _("购物数量"),
        required = True
    )

class DeclareForm(forms.Form):
    """
    报单表单
    """
    def get_level_money():
        level_money = []
        from TripleMag.apps.management.models import member_lv_money
        MemLevel = member_lv_money.objects.all()
        for ml in MemLevel:
            _level_money = []
            _level_money.append(ml.money)
            _level_money.append(ml.money)
            level_money.append(_level_money)
        return level_money
    declare_style = forms.ChoiceField(
        label = _("报单类型"),
        widget = forms.Select(), 
        choices = get_level_money(), 
        initial='1'
    )
    password_2nd = forms.CharField(
        label = _("二级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)
        super(DeclareForm, self).__init__(*args, **kwargs)
    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        verify_result = verify_password_2nd(password_2nd,self.user)
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd
        
    
class ChargeForm(forms.Form):
    """
    报单账户充值
    """
    amount = forms.DecimalField(
        label = _("充值金额"),
        widget = forms.TextInput(),
        required = True
    )


class AddressForm(ModelForm):
    """
    地址表单
    """
    is_primary = forms.BooleanField(
        required =False
    )
    class Meta:
        model = user_address
        exclude = ('user','is_primary')
        
    
