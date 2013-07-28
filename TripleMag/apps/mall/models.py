# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import  SelectMultiple
from django.forms.fields import MultipleChoiceField
from datetime import datetime

from TripleMag.apps.member.models import user_basic
from TripleMag.apps.member.models import user_address

##################################################################
#Mall fundamental category and product information
##################################################################

class Category(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False,unique=True,verbose_name='类目名最高级')
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='上传图片')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural ="最高级目录表"
class CategoryFirst(models.Model):
    name = models.CharField(max_length=30,null=False, blank=False,unique=True,verbose_name='类目名第二级')
    father_catagory = models.ForeignKey(Category,null=False,verbose_name='父类型')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural ="第二级目录表"
class CategorySecond(models.Model):
    name = models.CharField(max_length=30,null=False, blank=False,unique=True,verbose_name='类目名第三级')
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='上传图片')
    father_catagory = models.ForeignKey(CategoryFirst,null=False,verbose_name='父类型')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural ="第三级目录表"
class Product(models.Model):
    #Normal info.
    father_catagory = models.ForeignKey(CategorySecond,null=False,verbose_name='父类型')
    name = models.CharField(max_length=50,null=False,blank=False,unique=False,verbose_name='产品名')
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='上传图片')
    #Detail info.
    brand = models.CharField(max_length=30,null=True, blank=True,verbose_name='品牌')
    produced_at = models.CharField(max_length=30,null=True, blank=True,verbose_name='产地')
    package = models.CharField(max_length=30,null=True, blank=True,verbose_name='包装')
    details = models.TextField(null=False, blank=False,verbose_name='商品信息')
    after_sales = models.CharField(max_length=30,null=True, blank=True,verbose_name='售后服务')
    tip = models.CharField(max_length=250,null=True, blank=True,verbose_name='注意事项')
    #Amount info.
    total_num = models.IntegerField(null=False,blank=False,verbose_name='总量')
    sales = models.IntegerField(default=0,blank=True,null=False,verbose_name='销量')
    added_time = models.DateTimeField(auto_now_add=True,null=False, blank=True,verbose_name='上架时间')
    #is_reconmmend = models.IntegerField(null=False, blank=True,verbose_name='是否被推荐')
    #Modified at 7.14
    total_grade = models.PositiveIntegerField(null=False, blank=True,default=0,verbose_name='累积积分')
    recommender = models.ForeignKey(user_basic,null=False,blank=False,verbose_name='商品推荐人')
    #Modified at 7.16
    price_normal = models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False,verbose_name='市场价')
    price_VIP = models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False,verbose_name='商城价格')
    price_promotions = models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=True,default=0,verbose_name='促销价格')
    grade = models.PositiveIntegerField(null=False, blank=True,default=0,verbose_name='积分')
    bonus_stock = models.PositiveIntegerField(null=False, blank=False,default=0,verbose_name='赠股')
    start_time = models.DateTimeField(null=True, blank=True,verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True,verbose_name='结束时间')
    is_promoted = models.BooleanField(null=False,blank=False,verbose_name='是否被促销')
    #Modified at 8.14
    extra_price = models.DecimalField('运输额外费用',decimal_places=2,max_digits=10,null=False,blank=True,default=0)
    def __unicode__(self):
        return '\%s \%s' % (self.name, self.brand)
    class Meta:
        verbose_name_plural ="产品表"

class product_image(models.Model):
    product = models.ForeignKey(Product)
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='图片')
    class Meta:
        verbose_name_plural ="产品图片表"

##################################################################
#Mall order info
##################################################################

Order_Status= (
      ('finish','订单完成'),
      ('wait','等待处理'),
      ('sent','已经发货'),
      ('deny','已拒绝')
)

EnumTransWays= (
    ("self-pickup","上门自提"),
    ("EMS","EMS发送"),
    ("express","快递")
)

class Order(models.Model):
    user = models.ForeignKey(user_basic)
    address = models.ForeignKey(user_address)
    order_data = models.DateTimeField(auto_now_add=True,null=False, blank=True,verbose_name='订单生成日期')
    status = models.CharField(max_length=30,null=False, blank=False,choices = Order_Status,default="wait",verbose_name='订单状态')
    time_deal = models.DateTimeField(null=True,blank=True,verbose_name='订单处理时间')
    time_confirm = models.DateTimeField("订单确认收货时间",null=True,blank=True)
    transport_price = models.DecimalField('货物运输费用',max_digits=10,decimal_places=2,null=False,blank=False)
    transport_ways = models.CharField("配送方式",max_length=20,null=False,blank=False)
    transport_id = models.CharField("快递单号",max_length=40,null=True,blank=True)
    is_money_transfer = models.BooleanField('是否汇款付帐',null=False,blank=True,default=False)
    #Modified at 8.15
    contactor_name = models.CharField('联系人姓名',max_length=50,null=False,blank=False)
    contactor_phone = models.CharField('联系人手机号',max_length=13,null=False)
    def __unicode__(self):
        return self.coustom.telephone
    class Meta:
        verbose_name_plural ="订单表"

class shop_record(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    price = models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False,verbose_name='购物单价')
    quantity = models.IntegerField(null=False, blank=False,verbose_name='数量')
    evaluation = models.CharField(max_length=300,null=True,blank=True,verbose_name='评价')
    evalue_num = models.PositiveSmallIntegerField('评级',null=True, blank=True)
    class Meta:
        verbose_name_plural ="购物记录表"
        
class Collection(models.Model):
    user = models.ForeignKey(user_basic)
    product = models.ForeignKey(Product)
    class Meta:
        verbose_name_plural ="产品收藏表"
        
##################################################################
#Promotion info
##################################################################
#class Promotions(models.Model):
#    name = models.CharField(max_length=30,null=False, blank=False,verbose_name='促销活动表')
#    details = models.CharField(max_length=300,null=False, blank=False,verbose_name='促活动描述')
#    start_time = models.DateTimeField(auto_now_add=True,null=False, blank=False,verbose_name='开始时间')
#    end_time = models.DateTimeField(null=False, blank=False,verbose_name='结束时间')
#    image_url = models.CharField(max_length=100,null=False,blank=False,verbose_name='图片URL')
#    def __unicode__(self):
#        return self.name
#    class Meta:
#        verbose_name_plural ="促销活动表"

#class Promotions_Product(models.Model):
#    product = models.ForeignKey(Product)
#    normal_price = models.DecimalField(decimal_places=2,max_digits=10,null=False,blank=False,verbose_name='普通商城用户促销价格')
#    VIP_price = models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False,verbose_name='VIP商城用户促销价格')
#    promotion = models.ForeignKey(Promotions)
#    def __unicode__(self):
#        return self.product.name
#    class Meta:
#        verbose_name_plural ="促销产品表"

##################################################################
#Mall homepage
##################################################################

class mall_index(models.Model):
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='图片')
    product = models.ForeignKey(Product)
    class Meta:
        verbose_name_plural ="商城首页图片表"

class mall_ad(models.Model):
    image_url = models.ImageField(upload_to="static/images",null=True, blank=True,verbose_name='图片')
    product = models.ForeignKey(Product,null=True)
    class Meta:
        verbose_name_plural ="商城首页广告栏表"

class mall_prod_combination(models.Model):
    product = models.ForeignKey(Product,null=False)
    size = models.CharField('商品大小',max_length=30,null=True)
    color = models.CharField('商品颜色',max_length=10,null=True)
    class Meta:
        verbose_name_plural ="商城商品聚合表"
