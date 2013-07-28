# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

from TripleMag.apps.management.models import member_lv_money

##################################################################
#Fundamental user connections
##################################################################

EnumMemberType=(
    ("MemMax","报单中心"),
    ("MemMid","会员"),
    ("MemMin","商城用户"),
    ("MinVIP","商城VIP用户"),
)

class user_basic(models.Model):
    #user = models.ForeignKey()
    #user name might be the same as the number
    user = models.OneToOneField(User)
    number = models.CharField(max_length=8,null=False,blank=False,unique=True,verbose_name='编号')
    name = models.CharField(max_length=30,null=False,blank=False,verbose_name='姓名')
    role = models.CharField(max_length=6,null=False,blank=True,choices = EnumMemberType,verbose_name='用户类型')
    password_1nd = models.CharField(max_length=200,null=False,blank=False,verbose_name='一级密码')
    password_2nd = models.CharField(max_length=200,null=False,blank=False,verbose_name='二级密码')
    id_card_number = models.CharField(max_length=20,null=True,blank=True,verbose_name='身份证号码')
    phone = models.CharField(max_length=20,null=True,verbose_name='固定电话')
    mobile = models.CharField(max_length=13,null=True,verbose_name='手机')
    gender = models.CharField(max_length=1,null=False,default="M",choices=( ("M","男") , ("F","女")),verbose_name='性别')
    start_date = models.DateField (default=datetime.now,null=False,blank=True,verbose_name='会员注册日期')
    QQ = models.CharField(max_length=20,null=True,verbose_name='QQ号')
    is_void = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否为空点')
    is_stock_XR = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否被股票除权')
    is_blocked = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否被冻结')
    #IP_address = models.IPAddressField(verbose_name='用户最后一次登录时的IP地址')
    #login_time = models.DateTimeField(null=False,auto_now_add=True,verbose_name='用户最后一次登录时间')
    #Things below needs validation.
    #To mid/max user they need to enter all the info. so it's bonded in front-end.
    bank_name = models.CharField(max_length=20,null=True,verbose_name='开户银行')
    bank_account_id = models.CharField(max_length=40,null=True,verbose_name='银行卡号')
    bank_account_name = models.CharField(max_length=20,null=True,verbose_name='开户姓名')
    #Things below are all accounts.
    cash = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='现金账户余额')
    store_order = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='报单账户余额')
    store_cash = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='订货账户余额')
    stock_repeat = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='重复消费账户余额')
    stock_rebuy = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=True,default=0,verbose_name='回购账户余额')
    stock_hold = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='股票自有账户余额（持有股数）')
    #Web-A
    #Things below are accumulating during time.
    mall_single_score = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='商城团队积分')
    mall_team_score = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='商城个人积分')
    store_total_money_A = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='A区累积业绩')
    store_total_money_B = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='B区累积业绩')
    sum_declare = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='产品销售业绩累积值')
    sum_bonus_recost = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='产品销售回购奖累积值')
    #Web-B
    #Things below are different stock accounts
    stock_hold_0devide = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='零次拆股股数')
    stock_hold_1devide = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='一次拆股股数')
    stock_hold_2devide = models.PositiveIntegerField(null=False,blank=True,default=0,verbose_name='二次拆股股数')
    can_devide = models.BooleanField(null=False,blank=True,default=True,verbose_name='是否能享受拆股')
    stock_hold_max = models.PositiveIntegerField(null=True,blank=True,default=2500000,verbose_name='股票享受拆股封顶值')
    stock_sum = models.DecimalField('股票交易额',max_digits=10,decimal_places=2,null=False,blank=True,default=0)
    #Web-C
    #Things below are for calculating the proxy address
    proxy_area = models.CharField(max_length=20,null=True,verbose_name='代理区/县')
    proxy_city = models.CharField(max_length=20,null=True,verbose_name='代理城市')
    proxy_province = models.CharField(max_length=20,null=True,verbose_name='代理省份')
    can_share_out = models.BooleanField(null=False,blank=True,default=True,verbose_name='是否能享受商品分红')
    class Meta:
        verbose_name_plural ="基础用户信息表"

######################################################################
#Mid or higher user connections and values
######################################################################

#A L/M member have more data in advance
class user_mid_mem(models.Model):
    user = models.ForeignKey(user_basic,unique=True,null=False,verbose_name='用户ID')
    #The style of the id card number is bonded in front-end
    init_money = models.IntegerField(null=False,verbose_name='启动资金')
    level = models.ForeignKey(member_lv_money,null=False,verbose_name='等级ID')
    #has_applied_upgrade = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否已申请报单中心') 
    class Meta:
        verbose_name_plural ="会员信息表"

#A L member is a store, also have some data in advance
class user_max_mem(models.Model):
    user_mid = models.ForeignKey(user_mid_mem,unique=True,null=False,blank=False,verbose_name='会员ID')
    is_central = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否为中心店')
    #central is a state that have more commission than usual one.
    class Meta:
        verbose_name_plural ="报单中心信息表"

######################################################################
#Connections
######################################################################
#A table that solves the self-referring relationship
class user_adder(models.Model):
    added = models.ForeignKey(user_basic,related_name="user_add_from",null=False,verbose_name='添加者（报单中心）')
    adding = models.ForeignKey(user_basic,related_name="user_add_to",null=False,verbose_name='被添加者（会员）')
    class Meta:
        verbose_name_plural ="报单中心添加用户表"

#A table that solves the self-referring relationship
#The user should be more than a min member to get a recommender
#TBD
class user_recommender(models.Model):
    recommended = models.ForeignKey(user_basic,related_name="user_rec_from",unique=True,null=False,verbose_name='被推荐者')
    recommending = models.ForeignKey(user_basic,related_name="user_rec_to",null=False,verbose_name='推荐人')
    class Meta:
        verbose_name_plural ="推荐人关系表"

EnumContactedArea=(
    ("A","A区"),
    ("B","B区"),
)

#A table that solves the self-referring relationship
#TBD
class user_contactor(models.Model):
    contacted = models.ForeignKey(user_basic,related_name="user_cont_to",unique=True,null=False,verbose_name='被接点人')
    contacting = models.ForeignKey(user_basic,related_name="user_cont_from",null=False,verbose_name='接点人')
    contact_area = models.CharField(max_length=1,choices=EnumContactedArea,null=False,blank=False,verbose_name='所在区块')
    class Meta:
        verbose_name_plural ="接点人关系表"

#This indicates the relationship between central store and usual store.
class user_central_usual(models.Model):
    user_central = models.ForeignKey(user_max_mem,related_name="usr_central",unique=False,null=False,blank=False,verbose_name='中心店')
    user_usual = models.ForeignKey(user_max_mem,related_name="usr_usual",unique=True,null=False,blank=False,verbose_name='社区店')
    class Meta:
        verbose_name_plural ="中心店-社区店聚集关系表"

######################################################################
#Other informations
######################################################################

#A member have multiple addresses
class user_address(models.Model):
    user = models.ForeignKey(user_basic,null=False,verbose_name='用户ID')
    street = models.CharField(max_length=100,null=False,verbose_name='街道')
    #<=50 Chinese characters
    area = models.CharField(max_length=20,null=False,verbose_name='区/县')
    city = models.CharField(max_length=20,null=False,verbose_name='城市')
    province = models.CharField(max_length=20,null=False,verbose_name='省份')
    zip_code = models.CharField(max_length=20,null=False,verbose_name='邮编')
    is_primary = models.BooleanField(null=False,blank=True,default=False,verbose_name='是否为首要地址')
    class Meta:
        verbose_name_plural ="用户地址表"

EnumWithdrawState= (
    ("wait","等待处理"),
    ("sure","已受理"),
    ("deny","已拒绝"),
)

#Information modify 
class user_modify_record(models.Model):
    user = models.ForeignKey(user_basic,null=False,verbose_name='用户ID')
    name = models.CharField(max_length=30,null=True,blank=True,verbose_name='姓名')
    bank_name = models.CharField(max_length=20,null=True,verbose_name='开户银行')
    bank_account_id = models.CharField(max_length=40,null=True,verbose_name='银行卡号')
    bank_account_name = models.CharField(max_length=20,null=True,verbose_name='开户姓名')
    id_card_num = models.CharField(max_length=20,null=True,verbose_name='身份证号')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='申请时间')
    state = models.CharField(max_length=4,null=False,blank=True,choices=EnumWithdrawState,default="wait",verbose_name='状态')
    class Meta:
        verbose_name_plural ="会员修改信息申请表"

class member_mid_upgrade_record(models.Model):
    user = models.ForeignKey(user_basic,unique=True,null=False,verbose_name='用户ID')
    apply_time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='申请时间')
    grant_time = models.DateTimeField(null=True,blank=True,verbose_name='批准时间')
    upgrade_amount = models.PositiveIntegerField("升级所用额度",null=False,blank=True,default=0)
    state = models.CharField(max_length=4,null=False,blank=True,choices=EnumWithdrawState,default="wait",verbose_name='状态')
    class Meta:
        verbose_name_plural ="会员升级报单中心申请表"

class min_upgrade_record(models.Model):
    user = models.ForeignKey(user_basic,unique=True,null=False,verbose_name='用户ID')
    time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='申请时间')
    name = models.CharField(max_length=30,null=False,blank=False,verbose_name='姓名')
    bank_name = models.CharField(max_length=20,null=False,verbose_name='开户银行')
    bank_account_id = models.CharField(max_length=40,null=False,verbose_name='银行卡号')
    bank_account_name = models.CharField(max_length=20,null=False,verbose_name='开户姓名')
    state = models.CharField(max_length=4,null=False,blank=True,choices=EnumWithdrawState,default="wait",verbose_name='状态')
    class Meta:
        verbose_name_plural ="商城用户升级VIP申请表"

##################################################################
#Message board
##################################################################
class message(models.Model):
    user = models.ForeignKey(user_basic,null=False,blank=False)
    content = models.TextField(max_length=600,null=False,blank=False,verbose_name="留言内容")
    publish_time = models.DateTimeField(null=False,blank=True,auto_now=True,verbose_name='发布时间')
    reply = models.CharField(max_length=600,null=True,blank=True,verbose_name="管理员回复")
    reply_time = models.DateTimeField(null=True,blank=True,auto_now=True,verbose_name='管理员回复时间')
    class Meta:
        verbose_name_plural ="留言表"

##################################################################
#Shuffle ID
##################################################################
class shuffle_ID(models.Model):
    number = models.CharField(max_length=8,null=False,blank=False)
    class Meta:
        verbose_name_plural ="随机ID表"
