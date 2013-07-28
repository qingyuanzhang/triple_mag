#coding=utf-8
from django.shortcuts import render_to_response,HttpResponseRedirect,redirect
from django.template import Context, Template,RequestContext
from django.http import Http404

import json 
import sys,threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from TripleMag.apps.member.models import user_basic
from TripleMag.apps.management.models import value_setting
from django.core.urlresolvers import reverse
import time
def get_user_basic(fuc):
    #获取user_basic
    def new_get_user_basic(request,*args,**kwargs):
        user_number = request.GET.get("user_number",None)
        try:
            UserBasic = user_basic.objects.filter(number = user_number)[0]
            print UserBasic
        except:
            UserBasic = None
        return fuc(request,UserBasic = UserBasic,**kwargs)
    return new_get_user_basic
    
def admin_required(fuc):
    """
    验证管理员登录
    """
    def new_fuc(request, **kwargs):
        if request.user.first_name !="finance" and not request.user.is_superuser:
            raise Http404
        return fuc(request,**kwargs)
    return new_fuc

def admin_or_store_required(fuc):
    """
    管理员或者报单中心
    """
    def new_fuc(request, **kwargs):
        role = request.session.get('role',None)
        if role == "MemMax":
            MemMax = user_basic.objects.filter(user = request.user)[0]

            return fuc(request, Mem = MemMax, role="MemMax",**kwargs)
        elif role == "Admin":
            try:
                user_number =request.GET.get("user_number")
                MemMax = user_basic.objects.get(number = user_number)
            except:
                MemMax = None
            return fuc(request,Mem = MemMax, role="Admin",**kwargs)
        else:
            raise Http404
        
    return new_fuc
def store_required(fuc):
    """
    验证报单中心登录
    """
    def new_fuc(request, **kwargs):
        role = request.session.get('role',None)
        if role != "MemMax":
            raise Http404
        MemMax = user_basic.objects.filter(user = request.user)[0]
        return fuc(request,Mem = MemMax,**kwargs)
    return new_fuc
    
def mem_required(fuc):
    """
    验证会员登录
    """
    def new_fuc(request, **kwargs):
        try:
            MemMid = user_basic.objects.filter(user = request.user)[0]
            print request.session.get("role"),'llll'
            print request.session.get("password_2nd"),'lllllllf'
        except:
            raise Http404
        MemMid.sum = MemMid.cash + MemMid.stock_rebuy + MemMid.stock_repeat
        return fuc(request,Mem = MemMid,**kwargs)
    return new_fuc
    
def stock_locked(fuc):
    """
    股票封闭期
    """
    
    def new_fuc(request, **kwargs):
        

        UserBasic = kwargs.pop("Mem")
        time_now=time.localtime()
        error_detail = ""
        time_h =time.strftime("%H",time_now)
        time_m = time.strftime("%M",time_now)
        week_day = int(time.strftime("%w",time_now))
        print time_h,time_m
        time_able = int(time_h)*100 + int(time_m)
        VSetting = value_setting.objects.filter(stock_start_date__lte = week_day,stock_end_date__gte = week_day,stock_start_time__lte = time_able,stock_end_time__gte = time_able)
        print week_day,time_able
        UserBasic.stock_hold = UserBasic.stock_hold_0devide+UserBasic.stock_hold_1devide+UserBasic.stock_hold_2devide
        warning_1 = '您目前持有的股票总量为%s,股票回购账户余额为%s,股票重复消费额账户余额为%s'%(UserBasic.stock_hold,UserBasic.stock_rebuy,UserBasic.stock_repeat)
        warning_2 = ""
        able = True
        ValueSetting = value_setting.objects.all()[0]
        if not VSetting:
            error_name = '不在股票贩卖时间'
            error_detail = '对不起，当前股票系统不在股票正常贩卖时间,股票交易时间段为周%s到周%s的%s:%s到%s:%s' % (str(ValueSetting.stock_start_date),str(ValueSetting.stock_end_date),str(ValueSetting.stock_start_time/100),str(ValueSetting.stock_start_time % 100),str(ValueSetting.stock_end_time/100),str(ValueSetting.stock_end_time%100))
                           
            print error_detail
            able = False
            
        elif UserBasic.is_stock_XR:
            error_name = '被除权'
            error_detail = '对不起，您的股票账户已被除权，所有跟股票有关的账户均被冻结。'
            warning_2 = '请与管理员进行联系，以进行下一步的操作。'
            able = False
        elif ValueSetting.stock_lock_start:
            from datetime import timedelta
            stock_lock_end =ValueSetting.stock_lock_start + timedelta(days=ValueSetting.stock_locked_days)
            error_name = "股票封闭期"
            error_detail = "对不起，当前股票系统正在封闭期。封闭期结束的时间日期为%s,请届时再来查看"%(stock_lock_end)
            able = False
        elif not ValueSetting.switch_stock:
            error_name = "股票系统关闭"
            error_detail = "对不起，当前股票系统已被关闭。在系统被打开前均无法进行交易。"
            able = False
        if not able:
            template_name = "error.html"
            base = "stock/base.html"
            ctx = {
                'base': base,
                'error_name':error_name,
                'error_detail':error_detail,
                'warning_1':warning_1,
                'warning_2':warning_2
            }
            return render_to_response(template_name, RequestContext(request,ctx))
            return HttpResponseRedirect("/")
#        
        
        return fuc(request,Mem = UserBasic,error_detail = error_detail,**kwargs)
    return new_fuc

def stock_error(request,ctx,template_name):
    return render_to_response(template_name,RequestContext(ctx,template_name))
    

def can_member_login(fuc):
    """
    判断会员登录的装饰器
    """
    def new_fuc(request, **kwargs):
        if request.method =="POST" and not request.user.is_superuser:
            ValueSetting = value_setting.objects.defer("switch_member_login").all()[0]
            
            if not ValueSetting.switch_member_login and not request.user.is_superuser:
                template_name="error.html"
                base = "mall/login-base.html"
                error="……对不起，本网站正在维护中。"
                ctx = {
                    'error':error,
                    'base':base
                }
                return render_to_response(template_name,RequestContext(request,ctx))
        return fuc(request,**kwargs)
    return new_fuc

def can_store_declare(fuc):
    """
    判断报单功能装饰器
    """
    def new_fuc(request,**kwargs):
        if request.method == "POST":
            ValueSetting = value_setting.objects.defer("switch_store_declare").all()[0]
            if not ValueSetting.switch_store_declare:
                template_name = "store/base.html"
                error="网站正在维护中，报单中心的相应功能不开放。"
                
                ctx = {
                    "error":error
                }
                return render_to_response(template_name,RequestContext(request,ctx))
            
        return fuc(request, **kwargs)
    return new_fuc
def can_mall(fuc):
    """
    商城总开关
    """
    def new_fuc(request, **kwargs):
        ValueSetting = value_setting.objects.defer("switch_mall").all()[0]
        
        if not ValueSetting.switch_mall and not request.user.is_superuser:
            template_name="error.html"
            base = "mall/login-base.html"
            error = "……对不起，本网站正在维护中。"
            ctx = {
                'error':error,
                'base':base
            }
            return render_to_response(template_name,RequestContext(request,ctx))
        return fuc(request, **kwargs)
    return new_fuc
    
def can_member_register(fuc):
    """
    商城注册开关
    """
    def new_fuc(request, **kwargs):
        ValueSetting = value_setting.objects.defer("switch_mall_sign_in").all()[0]
        if not ValueSetting.switch_mall_sign_in:
            template_name="error.html"
            base = "mall/login-base.html"
            error = "网站正在维护中，商城注册功能不开放。"
            ctx = {
                "error":error,
                'base':base
            }
            return render_to_response(template_name,RequestContext(request,ctx))
        return fuc(request, **kwargs)
    return new_fuc

    
#    <div class="product-list-line">
#    	<h1>
#        	网站正在维护中，股票交易功能不开放。
#        </h1>
#    </div>
#    <div class="product-list-line">
#    	<h1>
#        	网站正在维护中，报单中心的相应功能不开放。
#        </h1>
#    </div>
#    <div class="product-list-line">
#    	<h1>
#        	网站正在维护中，商城注册功能不开放。
#        </h1>
#    </div>
#    <div class="product-list-line">
#    	<h1>
#        	……对不起，本网站正在维护中。
#        </h1>
#    </div>
        
        


