# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

from TripleMag.apps.member.models import user_basic
from TripleMag.apps.member.models import user_mid_mem
from TripleMag.apps.member.models import user_max_mem
from TripleMag.apps.member.models import member_lv_money

##################################################################
#Cash transmit record
##################################################################

#Transmit record
#This transaction is something without authorization, so it can be done immediatly.
class cash_trans(models.Model):
    user_from = models.ForeignKey(user_basic,related_name="usr_trans_from",null=False,blank=True,verbose_name='转账者ID')
    user_to = models.ForeignKey(user_basic,related_name="usr_trans_to",null=False,blank=False,verbose_name='到帐者ID')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='金额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='转账时间')
    class Meta:
        verbose_name_plural ="用户互转记录表"

#Withdraw deposit record
#Without a time_authorize and has_dealt is null, it's a unhandled request for withdraw deposit.
EnumWithdrawState= (
    ("wait","等待处理"),
    ("sure","已受理"),
    ("deny","已拒绝"),
)

class cash_withdraw(models.Model):
    user = models.ForeignKey(user_basic,null=False,verbose_name='用户ID')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='提现数额')
    time_start = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='提现请求时间')
    time_authorize = models.DateTimeField(null=True,blank=True,verbose_name='提现受理时间')
    state = models.CharField(max_length=4,null=False,blank=True,choices=EnumWithdrawState,default="wait",verbose_name='状态')
    class Meta:
        verbose_name_plural ="用户提现记录表"

##################################################################
#Declare and booking record for store
##################################################################

#Store account recharge record
class store_recharge_record(models.Model):
    max = models.ForeignKey(user_max_mem,null=False,verbose_name='用户ID')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='报单账户充值数额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='充值时间')
    class Meta:
        verbose_name_plural ="报单中心充值记录表"

#Store account declare record
class store_declare_record(models.Model):
    max = models.ForeignKey(user_max_mem,null=False,verbose_name='用户ID')
    amount = models.PositiveIntegerField(null=False,blank=False,verbose_name='报单数额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='报单时间')
    checked = models.BooleanField(null=False,blank=True,default=False)
    #Shows that whether the bonus of this declare record has been checked.
    #Once checked, one TERM has passed. ++TERM
    class Meta:
        verbose_name_plural ="报单中心报单记录表"

##################################################################
#Bonus record
##################################################################
class pre_count_declare(models.Model):
    max = models.ForeignKey(user_max_mem,null=False,verbose_name='用户ID')
    amount = models.PositiveIntegerField(null=False,blank=False,verbose_name='日累积数额')
    date = models.DateField(null=False,blank=True,auto_now=True,verbose_name='报单日期')
    class Meta:
        verbose_name_plural ="日累积临时记录表"

#Record the bonus type
EnumBonusType= (
    ("recharge","现金充值"),
    #Recharge the cash account
    #Don't use anymore.
    
    ("declare","服务费"),
    ("group","销售奖"),
    ("recost","回本奖"),
    ("comhelp","互助奖"),
    #Upper bonuses come from declaration.
    
    ("retail","消费奖"),
    ("summit","平级奖"), 
    ("recommend","推荐奖"),
    ("agent","代理奖"),
    #Upper bonuses come from shopping in mall.
    
    ("stock_return","股票贩卖返给推荐人"),
    #An stock bonus is something that's gonna get in the (recommender of the seller's) account instantly.
    #Don't use anymore.
)

#This is a recording table that save all the incoming bonus and their type.
#Record won't accumulate, they duplicate.
#Before paying the bonus, DBMS will search about all the value related and add them up.
class bonus_unpaid(models.Model):
    #declare = models.ForeignKey(store_declare_record,null=False)
    to_user = models.ForeignKey(user_basic,related_name="user_pay_to",null=False,verbose_name='得到奖金用户ID')
    type = models.CharField(max_length=10,null=False,choices=EnumBonusType,verbose_name='奖金类型')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='奖金数额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='奖金到达时间')
    cause_user = models.ForeignKey(user_basic,related_name="user_cause",null=False,verbose_name='触发奖金用户ID')
    paid = models.BooleanField("是否已发放",null=False,blank=True,default=False)
    
    #'Cause User' is defined as follows
    # declare - the user
    # group   - the user
    # recost  - the user
    # comhelp - the user's recommender
    # retail  - the user or the one whom the user recommended directly or indirectly
    # summit  - the one whom the user recommended directly or indirectly
    # stock   - the one whom the user recommended directly
    class Meta:
        verbose_name_plural ="奖金细目记录表"

#These record bonus by TERM. In one TERM the bonus will duplicate.
#After paying the bonus, this table keep record of the paying detail.
class bonus_declare_record(models.Model):
    mid = models.ForeignKey(user_mid_mem,null=False,verbose_name='用户ID')
    bonus_declare = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='服务费')
    bonus_group = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='销售奖')
    bonus_recost = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='回本奖')
    bonus_comhelp = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='互助奖')
    #Things below are summarization.
    tax = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='抽税')
    bonus_repeat = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='重复消费')
    #Bonus repeat: This part of money will flow into his stock repeat account(virtual).
    total = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='总计到帐金额')
    #Upper bonus flows into his cash account
    time = models.DateField(null=False,blank=True,auto_now=True,verbose_name='奖金到帐时间')
    counter = models.PositiveIntegerField(null=False,verbose_name='期数')
    class Meta:
        verbose_name_plural ="产品销售奖金发放记录表"

class bonus_mall_record(models.Model):
    user = models.ForeignKey(user_basic,null=False,verbose_name='用户ID')
    bonus_retail = models.DecimalField(max_digits=12,decimal_places=2,null=False,blank=True,default=0,verbose_name='消费奖')
    bonus_summit = models.DecimalField(max_digits=12,decimal_places=2,null=False,blank=True,default=0,verbose_name='平级奖')
    bonus_recommend = models.DecimalField('推荐奖',max_digits=12,decimal_places=2,null=False,blank=True,default=0)
    bonus_proxy = models.DecimalField('代理奖',max_digits=12,decimal_places=2,null=False,blank=True,default=0)
    #Things below are summarization.
    tax = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='抽税')
    total = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='总计到帐金额')
    #Upper bonus flows into his cash account
    time = models.DateField(null=False,blank=True,auto_now=True,verbose_name='奖金到帐时间')
    counter = models.PositiveIntegerField(null=False,verbose_name='期数')
    class Meta:
        verbose_name_plural ="C网奖金发放记录表"

EnumExtraBonusType= (
    #Site-C bonus:
    ("house","房奖"),
    ("car","车奖"),
    ("travel","旅游奖"),
    ("share","分红奖"),
    ("love","爱心奖"),
    #Upper bonuses don't go to user's account immediately
)
class extra_bonus(models.Model):
    to_user = models.ForeignKey(user_basic,related_name="usr_pay_extra_to",null=True,verbose_name='得到奖金用户ID')
    type = models.CharField(max_length=10,null=False,choices=EnumExtraBonusType,verbose_name='不直接发放奖金类型')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False,verbose_name='奖金数额')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='奖金到达时间')
    cause_user = models.ForeignKey(user_basic,related_name="usr_extra_cause",null=True,verbose_name='触发奖金用户ID')
    class Meta:
        verbose_name_plural ="不直接发放奖金记录表"

class day_perform_record(models.Model):
    mid = models.ForeignKey(user_mid_mem,null=False,verbose_name='用户ID')
    accumulate_a = models.PositiveIntegerField("A区业绩值",null=False)
    accumulate_b = models.PositiveIntegerField("B区业绩值",null=False)
    accumulate_self = models.PositiveIntegerField("报单",null=False)
    date = models.DateField(null=False,blank=True,auto_now=True,verbose_name='业绩计算日期')
    class Meta:
        verbose_name_plural ="每日业绩记录表"
