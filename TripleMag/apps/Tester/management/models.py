# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

##################################################################
#File download
##################################################################
class file_upload(models.Model):
    title =  models.CharField(max_length=30,null=False,blank=False,verbose_name="文件标题")
    url = models.FileField(upload_to="static/files",null=False,blank=False,verbose_name="文件地址")
    detail = models.TextField(null=True,blank=True,verbose_name="文件详细说明")
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='发布时间')
    class Meta:
        verbose_name_plural ="资料表"

##################################################################
#Notices
##################################################################

class notice_main(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False,verbose_name="公告标题")
    details = models.TextField(verbose_name="公告内容")
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='发表时间')
    class Meta:
        verbose_name_plural ="主页公告表"

class notice_mall(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False,verbose_name="公告标题")
    details = models.TextField(verbose_name="公告内容")
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='发表时间')
    class Meta:
        verbose_name_plural ="商城公告表"

##################################################################
#All the rate settings
##################################################################

#A L/M member have level number that indicates his initial fund
class member_lv_money(models.Model):
    name = models.CharField(max_length=14,null=False,blank=False,verbose_name='等级会员名称')
    level = models.PositiveSmallIntegerField(null=False,blank=False,verbose_name='等级')
    money = models.IntegerField(null=False,blank=False,verbose_name='金额')
    low_percentage = models.DecimalField(max_digits=2,decimal_places=2,null=False,blank=False,verbose_name='小区')
    day_max = models.PositiveIntegerField(null=False,blank=False,verbose_name='日封顶')
    #This money show how many money a L/M paid when signed in.
    class Meta:
        verbose_name_plural ="会员等级-接点人关系表"

class mall_level(models.Model):
    level_name = models.CharField(max_length=20,null=False,blank=False,verbose_name='级别名称')
    min_score = models.PositiveIntegerField(null=False,blank=False,verbose_name='该等级团队最小积分')
    max_score = models.PositiveIntegerField(null=False,blank=False,verbose_name='该等级团队最大积分')
    threshold_value = models.PositiveIntegerField(null=False,blank=False,verbose_name='个人最少零售业绩')
    gain_rate = models.DecimalField(max_digits=2,decimal_places=2,null=False,blank=False,verbose_name='得到利润')
    class Meta:
        verbose_name_plural = "商城积分等级-利润表"
    
class mall_summit(models.Model):
    summit_num = models.SmallIntegerField(null=False,blank=False)
    bonus_percent = models.DecimalField(null=False,blank=False,max_digits=2,decimal_places=2)
    class Meta:
        verbose_name_plural = "同级部门数量-平级奖比例表"

##################################################################
#All setting value in one group
##################################################################
class value_setting(models.Model):
    #--------------------------
    #Trial setting
    #--------------------------
    trial_left_days = models.PositiveIntegerField(null=True,default=1000,verbose_name='试运营剩余日期')
    #--------------------------
    #Password setting
    #--------------------------
    password_1nd = models.CharField(max_length=20,null=False,blank=False,default='555666',verbose_name='默认一级密码')
    password_2nd = models.CharField(max_length=20,null=False,blank=False,default='555666',verbose_name='默认二级密码')
    #--------------------------
    #Stock setting
    #--------------------------
    sell_min_amount = models.PositiveIntegerField(null=False,default=1000,verbose_name='单次最少卖出股数')
    sell_max_amount = models.PositiveIntegerField(null=False,default=10000000,verbose_name='单次最多卖出股数')
    stock_tax_rate = models.DecimalField(max_digits=4,decimal_places=4,default=0.15,null=False,verbose_name='股票抽税比例')
    stock_repo_rate = models.DecimalField(max_digits=4,decimal_places=4,default=0.255,null=False,verbose_name='回购比例')
    stock_ex_return_rate = models.DecimalField(max_digits=4,decimal_places=4,default=0.0595,null=False,verbose_name='返给上级比例')
    stock_locked_days = models.PositiveSmallIntegerField(null=False,default=180,verbose_name='锁定期延续时长（天）')
    stock_lock_start = models.DateField(null=True,blank=True,verbose_name='锁定期开始日期')
    stock_value_now = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=1.00,verbose_name='当日股票单价')
    stock_value_delta = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.01,verbose_name='允许卖出价偏离单价量')
    stock_selling_days = models.PositiveSmallIntegerField(null=False,default=7,verbose_name='股票在卖出池中的延续时长（天）')
    stock_start_time = models.PositiveSmallIntegerField(null=False,default=930,verbose_name='股票开始时间（小时/每天）')
    stock_end_time = models.PositiveSmallIntegerField(null=False,default=1530,verbose_name='股票结束时间（小时/每天）')
    stock_start_date = models.PositiveSmallIntegerField(null=False,default=1,verbose_name='股票开始时间（星期/每周）')
    stock_end_date = models.PositiveSmallIntegerField(null=False,default=5,verbose_name='股票结束时间（星期/每周）')
    #A permitted selling value is between value_now +- value_delta
    P2P_radix = models.PositiveIntegerField(null=False,default=10000,verbose_name='点对点股票卖出基数')
    P2P_max = models.PositiveIntegerField(null=False,default=500000,verbose_name='点对点股票最多卖出数')
    stock_hold_max = models.PositiveIntegerField(null=True,default=2500000,verbose_name='最大持有拆股数')
    stock_share_out_min_amount = models.PositiveIntegerField(null=False,default=2500000,verbose_name='参与分红股票最小值')
    stock_share_out_min_trade = models.PositiveIntegerField(null=False,default=100000,verbose_name='参与分红交易额最小值')
    
    #The money amount that's able to sell is P2P_radix * N
    #--------------------------
    #Money and bonus setting
    #--------------------------
    bonus_tax_rate = models.DecimalField(max_digits=2,decimal_places=2,null=False,default=0.07,verbose_name='产品销售抽税比例')
    repo_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.093,verbose_name='重复消费比例')
    recost_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.05,verbose_name='回本奖比例')
    comhelp_1st_min = models.PositiveSmallIntegerField(null=False,default=1,verbose_name='一级互助奖直荐人数最小值')
    comhelp_1st_max = models.PositiveSmallIntegerField(null=False,default=2,verbose_name='一级互助奖直荐人数最大值')
    comhelp_2nd_min = models.PositiveSmallIntegerField(null=False,default=3,verbose_name='二级互助奖直荐人数最小值')
    comhelp_2nd_max = models.PositiveSmallIntegerField(null=False,default=4,verbose_name='二级互助奖直荐人数最大值')
    comhelp_3rd_min = models.PositiveSmallIntegerField(null=False,default=5,verbose_name='三级互助奖直荐人数最小值')
    comhelp_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.05,verbose_name='互助奖比例')
    withdraw_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.005,verbose_name='提现抽税')
    declare_central_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.05,verbose_name='中心店服务费')
    declare_normal_rate = models.DecimalField(decimal_places=4,max_digits=4,null=False,default=0.04,verbose_name='社区店服务费')
    #--------------------------
    #Mall setting
    #--------------------------
    mall_grade_rate = models.DecimalField(decimal_places=7,max_digits=14,null=False,default=0.001,verbose_name='商品价格换算积分率')
    #Range 999,9999~0.0000001 times of the price.
    mall_stock_rate = models.DecimalField(decimal_places=7,max_digits=14,null=False,default=1,verbose_name='积分换算股票率')
    #Range 999,9999~0.0000001 times of the price.
    #Never used it since 7.15
    grade_summit = models.PositiveIntegerField(null=False,default=6400,verbose_name='用户成为同级部门最小积分')
    mall_VIP_threshold = models.PositiveIntegerField(null=False,default=2000,verbose_name='商城用户成为VIP最小积分')
    #Changed at 8.08
    mall_love_rate = models.DecimalField("爱心奖比例",decimal_places=2,max_digits=2,null=False,default=0.04)
    mall_car_rate = models.DecimalField("车奖比例",decimal_places=2,max_digits=2,null=False,default=0.01)
    mall_house_rate = models.DecimalField("房奖比例",decimal_places=2,max_digits=2,null=False,default=0.02)
    mall_travel_rate = models.DecimalField("旅游奖比例",decimal_places=2,max_digits=2,null=False,default=0.01)
    mall_share_rate = models.DecimalField("分红奖比例",decimal_places=2,max_digits=2,null=False,default=0.10)
    mall_proxy_rate = models.DecimalField("代理奖比例",decimal_places=2,max_digits=2,null=False,default=0.06)
    mall_recommend_rate = models.DecimalField("推荐奖比例",decimal_places=2,max_digits=2,null=False,default=0.04)
    #Changed at 8.09
    mall_proxy_prov = models.DecimalField("省级代理奖比例",decimal_places=2,max_digits=2,null=False,default=0.06)
    mall_proxy_city = models.DecimalField("市级代理奖比例",decimal_places=2,max_digits=2,null=False,default=0.05)
    mall_proxy_area = models.DecimalField("县级代理奖比例",decimal_places=2,max_digits=2,null=False,default=0.04)
    mall_tax_rate = models.DecimalField(max_digits=4,decimal_places=4,default=0.075,null=False,verbose_name='C网奖金抽税比例')
    #--------------------------
    #Function switch
    #--------------------------
    switch_member = models.BooleanField(default=True,null=False,verbose_name='会员功能总开关')
    switch_member_login = models.BooleanField(default=True,null=False,verbose_name='会员登录开关')
    switch_member_transfer = models.BooleanField(default=True,null=False,verbose_name='会员互转开关')
    switch_stock = models.BooleanField(default=True,null=False,verbose_name='股票交易总开关')
    switch_store_declare = models.BooleanField(default=True,null=False,verbose_name='报单中心报单开关')
    switch_store_order = models.BooleanField(default=True,null=False,verbose_name='报单中心下订单开关')
    switch_store_add_user = models.BooleanField(default=True,null=False,verbose_name='报单中心添加会员开关')
    switch_mall = models.BooleanField(default=True,null=False,verbose_name='商城总开关')
    switch_mall_sign_in = models.BooleanField(default=True,null=False,verbose_name='商城注册开关')
    class Meta:
        verbose_name_plural ="全部基础设置表"
