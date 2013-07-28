# -*- coding:utf8 -*-
#sql_view
from django.db import models
from TripleMag.apps.member.models import user_basic
class UserView(models.Model):
    number = models.CharField(editable = False ,verbose_name='编号')
    name = models.CharField(editable = False ,verbose_name='姓名')
    start_date = models.DateField (editable = False ,verbose_name='会员注册日期')
    role = models.CharField(editable = False ,verbose_name='用户类型')
    recommending_id = models.CharField(editable = False ,verbose_name='推荐人编号')
    recommending_name = models.CharField(editable = False ,verbose_name = "推荐人姓名")
    contacting_id = models.CharField(editable = False ,verbose_name = "节点人编号")
    contacting_name = models.CharField(editable = False , verbose_name = "节点人姓名")
    is_void = models.CharField(editable = False ,verbose_name = "是否为空点")
    level = models.CharField(editable = False , verbose_name = "等级")
    
#class StoreInfo(UserView):
#    level = models.CharField(max_length=8,null=False,blank=False,verbose_name='用户等级')


class WithDrawView(models.Model):
    number = models.CharField(editable = False ,verbose_name='编号',primary_key=True)
    name =  models.CharField(editable = False ,verbose_name='姓名')
    bank_name = models.CharField(editable = False ,verbose_name='开户银行')
    bank_account_id = models.CharField(editable = False ,verbose_name='银行帐号')
    bank_account_name = models.CharField(editable = False ,verbose_name='开户姓名')
    cash = models.DecimalField(editable = False ,verbose_name='现金账户余额')
    mobile = models.CharField(editable = False ,verbose_name='手机')
    amount = models.DecimalField(editable = False ,verbose_name='提现金额')
    time_start = models.DateTimeField(editable = False ,verbose_name='提现申请时间')
    time_authorize = models.DateTimeField(editable = False ,verbose_name='提现受理时间')
    state = models.CharField(editable = False ,verbose_name='提现状态')
    class Meta:
         managed = False
         db_table = "WithDrawView"
         
         
         

    
