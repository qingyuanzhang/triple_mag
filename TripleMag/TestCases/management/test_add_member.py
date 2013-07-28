#coding=utf-8
from django.test import TestCase,Client
from TripleMag.apps.member.models import *

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from TripleMag.apps.management.views import add_member
class AddMemberTest(TestCase):
    def setUp(self):
        call_command('loaddata', 'fixtures/management/management.json', verbosity=0)
        
    def test_add_memeber(self):
        """
        测试未登录用户
        /management/add_member/
        """
        response = self.client.get(reverse("management_add_memeber"))
        self.assertEquals(response.status_code,302)
    
    def test_authenticated_add_member(self):
        """
        会员信息
        """
        data = {
            "number": "RT123456",
            "name": "张xx",
            "bank_account_id":"1111111111111",
            "password_1nd":"111111",
            "password_1nd_again":"111111",
            "password_2nd":"111111",
            "password_2nd_again":"111111",
            "role":"会员",
            "QQ":"11111111111",
            "phone":"11111111",
            "mobile":"1111111111",
            "gender":"M",
        }
        #测试添加会员
        self.client.login(username = 'zhangqingyuan',password = '111111')
        response = self.client.get(reverse("management_add_memeber"),data)
        self.assertEquals(response.status_code,200)
        """
        报单中心信息
        """
        data['store_id'] = "RT888888",
        data['level'] = "一级代理"
        #测试添加报单中心
        response = self.client.get(reverse("management_add_memeber"),data)
        self.assertEquals(response.status_code,200)
        self.logout()
        
#    def test_search_member(self):
        
        
        
        
        
        
        
        
        
        
        
    
    
    
