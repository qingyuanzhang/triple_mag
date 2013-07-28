# -*- coding:utf8 -*-
#sql_view
from django.db import models
from TripleMag.apps.member.models import user_basic,user_contactor,user_recommender,user_adder,user_mid_mem

#class MemberInfo(models.Model):
#    user_basic = models.ForeignKey(user_basic)
#    user_contactor = models.ForeignKey(user_contactor)
#    user_recommender = models.ForeignKey(user_recommender)
#    user_adder = models.ForeignKey(user_adder)
#    user_mid_mem = models.ForeignKey(user_mid_mem)
#    class Meta:
#         managed = False
#         

#class TestView(models.Model):
#    name = models.CharField(max_length=30,null=False,blank=False,verbose_name='姓名')
#    class Meta:
#         managed = False
         
