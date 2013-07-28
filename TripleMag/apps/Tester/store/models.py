# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

from TripleMag.apps.member.models import user_max_mem
from TripleMag.apps.member.models import user_address

##################################################################
#Fundamental store goods info
##################################################################

class stuff_type(models.Model):
    name = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='货物类型名称')
    detail = models.TextField(null=True,blank=True,verbose_name='货物类型简介')
    picture = models.ImageField(upload_to="static/images",null=True,verbose_name='货物类型图片')
    #to save icon's address
    class Meta:
        verbose_name_plural ="货物类型表"
    def __unicode__(self):
        return self.name
class stuff(models.Model):
    type = models.ForeignKey(stuff_type,null=False,verbose_name='货物类型ID')
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name='货物名称',unique=True)
    total_num = models.IntegerField(default=100,blank=True,verbose_name='总量')
    detail = models.TextField(null=True,blank=True,verbose_name='货物简介')
    price_single = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='货物单价')
    picture = models.ImageField(upload_to="static/images",null=True,verbose_name='货物图片')
    class Meta:
        verbose_name_plural ="货物详情表"

##################################################################
#Booking record for store
##################################################################
EnumOrderState= (
    ("wait","等待处理"),
    ("sure","确认发货"),
    ("deny","拒绝发货"),
    ("done","确认收货"),
)

class order(models.Model):
    max = models.ForeignKey(user_max_mem,null=False,verbose_name='报单中心ID')
    time_add = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='订单生成时间')
    time_deal = models.DateTimeField(null=True,blank=True,verbose_name='订单处理时间')
    state = models.CharField(max_length=4,null=False,blank=True,choices=EnumOrderState,default="wait",verbose_name='订单状态')
    address = models.ForeignKey(user_address,null=False,related_name='order_address_id',verbose_name='地址ID')
    #stuff = models.ForeignKey(stuff,null=False,blank=False,verbose_name='货物ID')
    class Meta:
        verbose_name_plural ="报单中心订单表"

class order_stuff(models.Model):
    order = models.ForeignKey(order,null=False,blank=False,verbose_name='订单ID')
    stuff = models.ForeignKey(stuff,null=False,blank=False,verbose_name='货物ID')
    amount = models.IntegerField(null=False,blank=False,verbose_name='货物数量')
    price_total = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='货物总价')
    class Meta:
        verbose_name_plural ="报单中心订单-商品表"
