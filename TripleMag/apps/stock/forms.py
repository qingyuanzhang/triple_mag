# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

import re
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms import ModelForm
from TripleMag.apps.stock.models import selling_poll,trade_record
from TripleMag.apps.management.models import value_setting
from TripleMag.apps.views import verify_password_2nd
class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)

#class SellStockForm(ModelForm):
#    #股票购买售出或则表单
#    password_2nd = forms.CharField(
#        widget = forms.PasswordInput(),
#        required = True
#    )
#    class Meta:
#        model = selling_poll
#        fields = ('user_from','time')
#        
class BuyStockForm(ModelForm):
    password_2nd = forms.CharField(
        widget = forms.PasswordInput(),
        required = True
    )
    n_seller = forms.CharField(
        label= _("卖出者"),
        widget = forms.TextInput(),
        required = False
    )
    class Meta:
        model = trade_record
        fields = ('amount','value',)
        

class StockForm(ModelForm):
    """
    股票表单
    """
    password_2nd = forms.CharField(
        widget = forms.PasswordInput(),
        required = True
    )
    n_seller = forms.CharField(
        label= _("卖出者"),
        widget = forms.TextInput(),
        required = False
    )
    class Meta:
        model = trade_record
        fields = ('amount','value',)
        
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("user",None)
        super(StockForm, self).__init__(*args, **kwargs)
        self.ValueSetting = value_setting.objects.all()[0]
    def clean_value(self):
        from decimal import *
        value = self.cleaned_data['value']
        min_stock_Value = self.ValueSetting.stock_value_now - self.ValueSetting.stock_value_delta
        if value < min_stock_Value:
            raise forms.ValidationError("您输入的价格小于当前的股票价格")
        else:
            return value
    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        verify_result = verify_password_2nd(password_2nd,self.user)
        if not verify_result:
            raise forms.ValidationError("二级密码错误")
        return password_2nd

    
