# -*- coding:utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm

from TripleMag.apps.member.models import *

class user_adderInline(admin.TabularInline):
    model = user_adder
    fk_name = "added"
class user_basic_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(BasicForm, self).__init__(*args, **kwargs)
    class Meta:
        model = user_adder
#    recommended = forms.CharField(
#        label = ("留言内容"),
#        max_length = 8,
#        widget = forms.TextInput()
#    )
class user_basicAdmin(admin.ModelAdmin):

    pass

#    inlines = [
#            user_adderInline,
#        ]
class user_adderAdmin(admin.ModelAdmin):
    pass

admin.site.register(user_basic,user_basicAdmin)

admin.site.register(user_adder,user_adderAdmin)
