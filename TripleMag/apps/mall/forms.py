# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError  

from TripleMag.apps.mall.models import *
from TripleMag.apps.management.forms import UserForm
from TripleMag.apps.management.models import notice_mall
from TripleMag.apps.mall.models import mall_index,mall_ad
from TripleMag.apps.member.models import user_basic
class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)
        
class EvaluationForm(BasicForm):
    #评价表单
    evaluation = forms.CharField(
        label = _("评价"),
        max_length = 300,
        widget = forms.TextInput(),
        required = True
    )
    score = forms.IntegerField(
        label = _("分数"),
        max_value = 100,
        min_value = 0,
        widget = forms.IntegerField(),
        required = True
    )
class ProductForm(ModelForm):
    #商品表单
    recommender = forms.CharField(
        label = _("推荐人"),
        max_length = 8,
        widget = forms.TextInput(),
        required = True,
        help_text = _("显示用户姓名")
    )
    class Meta:
        model = Product
#        fields = ("father_catagory","name","image_url",
#                  "brand","produced_at","package","details",
#                  "after_sales","tip","total_num","recommender","price_normal",
#                  "price_VIP")
        exclude = ("sales",'added_time','total_grade','recommender'
        )
    def clean_recommender(self):
        recommender = self.cleaned_data['recommender']
        Recommended = user_basic.objects.defer(None).filter(number = recommender)
        if not Recommended:
            raise forms.ValidationError("推荐人不存在")
        return recommender
class CategoryForm(ModelForm):
    """
    第一级目录表
    """
    class Meta:
        model = Category
        exclude =('image_url')
class CategoryFirstForm(ModelForm):
    """
    第二级目录表
    """
    class Meta:
        model = CategoryFirst
        exclude =('image_url')
class CategorySecondForm(ModelForm):
    """
    第三级目录表
    """
    class Meta:
        model = CategorySecond
        exclude =('image_url')

class RegisterForm(UserForm):
    is_void = forms.BooleanField(
        required=False,
        initial = False
    )
    
    role = forms.CharField(
        required=False,
        initial = "MemMin"
    )


class ChangePasswordForm(forms.Form):
    """
    修改密码表单
    """
    password = forms.CharField(
        label = _("一级密码"),
        widget = forms.PasswordInput(),
        required = False
    )
    new_password_again = forms.CharField(
        label = _("新一级密码确认"),
        widget = forms.PasswordInput(),
        required = False
    )
    
    new_password = forms.CharField(
        label = _("新一级密码"),
        widget = forms.PasswordInput(),
        required = False
    )

    def __init__(self, *args,**kwargs):
        self.UserBasic = kwargs.pop("UserBasic",None)
        self.user = kwargs.pop("user",None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
    def clean_new_password(self):   
        password = self.cleaned_data.get("password")
        new_password = self.cleaned_data["new_password"]
        new_password_again = self.cleaned_data.get("new_password_again")
        if new_password and new_password == new_password_again and password:
            password_check = self.user.check_password(password)
            if password_check:
                
                self.user.set_password(new_password)
                self.user.save()
                if not self.user.is_superuser and not self.user.first_name == "finance":
                    self.UserBasic.password_1nd = self.user.password
                    self.UserBasic.save()
                return new_password
            else:
                raise forms.ValidationError("密码错误")
        else:
            raise forms.ValidationError("请输入正确的密码")
        
class ChangePassword_2ndForm(forms.Form):

    password_2nd = forms.CharField(
        label = _("一级密码"),
        widget = forms.PasswordInput(),
        required = False
    )
    new_password_2nd_again = forms.CharField(
        label = _("新一级密码确认"),
        widget = forms.PasswordInput(),
        required = False
    )
    new_password_2nd = forms.CharField(
        label = _("新一级密码"),
        widget = forms.PasswordInput(),
        required = False
    )

    def __init__(self, *args,**kwargs):
        self.UserBasic = kwargs.pop("UserBasic",None)
        self.user = kwargs.pop("user",None)
        print self.user ,self.UserBasic
        super(ChangePassword_2ndForm, self).__init__(*args, **kwargs)
    
    def clean_new_password_2nd(self,*args, **kwargs):
        from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
        password = self.cleaned_data.get("password_2nd")
        new_password = self.cleaned_data["new_password_2nd"]
        new_password_again = self.cleaned_data.get("new_password_2nd_again")
        
        if password and new_password and new_password == new_password_again:
            result = check_password(password,self.UserBasic.password_2nd)
            if result:
                new_password = make_password(new_password)
                self.UserBasic.password_2nd = new_password
                self.UserBasic.save()
                return self.cleaned_data
            else:
                raise forms.ValidationError("密码不正确")
        else:
            raise forms.ValidationError("请输入正确的密码")
class NoticeMallForm(ModelForm):
    """
    商城公告表单
    """
    class Meta:
        model = notice_mall
        exclude = ('time')
        
class MallAdForm(ModelForm):
    """
    公告表单
    """
    class Meta:
        model = mall_ad
        
class MallIndexForm(ModelForm):
    """
    商城首页表单
    """
    class Meta:
        model = mall_index
        
    
    
