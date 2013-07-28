# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

from TripleMag.apps.member.models import user_basic

##################################################################
#Stock trade 
##################################################################

class selling_poll(models.Model):
    user_from = models.ForeignKey(user_basic,related_name="usr_from",null=False,verbose_name='卖出者用户ID')
    amount = models.IntegerField(null=False,verbose_name='卖出数量')
    value = models.DecimalField(max_digits=10,decimal_places=4,null=False,verbose_name='单价')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='进入卖出池时间')
    user_to = models.ForeignKey(user_basic,related_name="usr_to",null=True,verbose_name='定向卖给用户ID')
    #if user_to is null, then it's selled to everybody.
    #or only the user_to can see the selling
    #in the meanwhile the P2P selling have different setting of data
    #
    class Meta:
        verbose_name_plural ="卖出池表"

##################################################################
#Stock records 
##################################################################

class trade_record(models.Model):
    buyer = models.ForeignKey(user_basic,related_name="usr_buyer",null=False,verbose_name='买股者ID')
    seller = models.ForeignKey(user_basic,related_name="usr_seller",null=False,verbose_name='卖股者ID')
    amount = models.IntegerField(null=False,verbose_name='交易数量')
    value = models.DecimalField(max_digits=10,decimal_places=4,null=False,verbose_name='单价')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='成交时间')
    #What's following is info. for sellers
    tax = models.DecimalField(max_digits=10,decimal_places=2,null=False,verbose_name='抽税')
    repo = models.DecimalField(max_digits=10,decimal_places=2,null=False,verbose_name='回购')
    #Repo is the money that returns to his rebuy account to encourage him to buy more stock.
    ex_return = models.DecimalField(max_digits=10,decimal_places=2,null=False,verbose_name='返给上级')
    #Return to the seller's recommender
    gain = models.DecimalField(max_digits=10,decimal_places=2,null=False,verbose_name='卖者最后所得')
    class Meta:
        verbose_name_plural ="股票交易记录表"



#class flowing_stock(models.Model):
#    amont = models.BigIntegerField(null=False)
#    def __unicode__(self):
#        return self.name
#    class Meta:
#        verbose_name_plural ="系统总股数"

EnumIncomeType= (
    ("recharge","自购充值"),
    ("gift","商城购买赠送"),
    ("buy","股票交易购买"),
)
class income_record(models.Model):
    to_user = models.ForeignKey(user_basic,related_name="usr_income",null=True,verbose_name='得到股票用户ID')
    type = models.CharField(max_length=10,null=False,choices=EnumIncomeType,verbose_name='股票得到途径')
    amount = models.DecimalField(max_digits=10,decimal_places=4,null=False,blank=False,verbose_name='股票数额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='股票到达时间')
    class Meta:
        verbose_name_plural ="股票收入表"

class trend_record(models.Model):
    value = models.DecimalField(max_digits=10,decimal_places=4,null=False,default=1.00,verbose_name='股票单价')
    day = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='日期')
    class Meta:
        verbose_name_plural ="趋势图表"
