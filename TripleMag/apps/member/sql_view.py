# -*- coding:utf8 -*-
#sql_view
from django.db import models
from TripleMag.apps.member.models import 


class MemberDetails(models.Model):
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
    
