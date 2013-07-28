#coding=utf8

import json 
import sys,threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#import simplejson as json
import json

from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.http import Http404
from TripleMag.apps.sql_view import test1
from TripleMag.apps.member.models import user_basic,user_contactor
from TripleMag.apps.decorators import get_user_basic
from notification.models import NoticeType,Notice
import csv
from django.http import HttpResponse
from TripleMag.apps.decorators import admin_or_store_required
from datetime import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from TripleMag.apps.management.models import value_setting
from TripleMag.apps.stock.models import trend_record
from TripleMag.apps.mall.models import product_image

from django.db import connection
import warnings
from warnings import filterwarnings
import MySQLdb as Database
filterwarnings('ignore', category = Database.Warning)

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        goto_url = reverse("management_index")
    elif user.first_name =="finance":
        goto_url = reverse("management_member_index")
    else:
        goto_url = reverse("member")
        
    return HttpResponseRedirect(goto_url)
    
def test(request):
#    from TripleMag.apps.stock.models import trade_record,selling_poll,income_record as t_income_record,trend_record
##    chart_data = "[['name','Manager','Tooltip'],['ART01',null,'father' ],[{v: 'BOOM01', f: 'BOOM01<br/><font color=\"red\"><i>业绩1000<i></font>'},'ART01',null],['Carol','BOOM01',     null]]"
##    template_name = "test.html"
##    ctx = {
##        'chart_data':chart_data
##    }
#    import time
#    TrendRecord = trend_record.objects.all()
#    ChartData = [["date","{{a}}"]]
#    for TRecord in TrendRecord:
#        day = str(TRecord.day)[0:10]  
#        _CharData = []
#        _CharData.append(day)
#        _CharData.append(float(TRecord.value))
#        ChartData.append(_CharData)
##    print str(ChartData)

    template_name = "test.html"
    ctx={
        "ChartData":""
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
@cache_page(60 * 15)
@get_user_basic
def get_user_name(request,**kwargs):

    UserBasic = kwargs.pop("UserBasic")
    if not UserBasic:
        data = "无此会员"
    else:
        data = UserBasic.name
    return HttpResponse(json.dumps(data),mimetype="application/json")
    
def change_one(request, authentication_form=AuthenticationForm):
    """
    换一张
    """
    form =  authentication_form(request)  
    print form
    template_name = "account/captcha.html"
    ctx = {
        "form": form
    }  
    return render_to_response(template_name, RequestContext(request, ctx))


def change_number(request, **kwargs):
    """
    换一个编号
    """
    number = get_number()
    return HttpResponse(json.dumps(number),mimetype="application/json")

    
class CallProc:
    """
    调用存储过程类
    """
    def __init__(self):
        self.cursor = connection.cursor()
#        self.cursor.execute("use `TripleMag`")
        print 'ssss555'
    def CallProcFuc_0(self,proc_name):
        """
        没有参数直接调用的存储过程
        """
        
        self.cursor.callproc(proc_name)
        print 'sss'
    def CallProcFuc_1(self,proc_name,val_1):
        """
        一个参数的存储过程
        """    
        
        self.cursor.callproc(proc_name,(val_1,))
        
    def CallProcFuc_2(self,proc_name,val_1,val_2):
        """
        两个参数的存储过程
        """
        print 'ssss6665'
        self.cursor.callproc(proc_name,(val_1,val_2,))
    def CallProcFuc_3(self,proc_name,val_1,val_2,val_3):
        """
        3个参数的存储过程
        """
        print proc_name,type(val_1),type(val_2),type(val_3)
        self.cursor.callproc(proc_name,(val_1,val_2,val_3,))
    def CallProcFuc_4(self,proc_name,val_1,val_2,val_3,val_4):
        """
        两个参数的存储过程
        """
        self.cursor.callproc(proc_name,(val_1,val_2,val_3,val_4,))
    def __del__(self):
#        connection.connection.commit()
        self.cursor.nextset()
        self.cursor.close()
        connection.close()

def PaginatorFuc(request,data,number=10):
    """
    翻页函数
    """

    paginator = Paginator(data, number)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1 
    try:
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)
    return data
        
def get_number():
    from django.db import connection
    var = ''
    cursor = connection.cursor()
    cursor.callproc("GetNewRandomId",(var,))
    cursor.execute('select @_GetNewRandomId_0')
    number = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return number
    
def verify_password_2nd(password_2nd,user):
    """
    二级密码验证
    """
    
    UserBasic = user_basic.objects.filter(user = user)
    if UserBasic:
        result = check_password(password_2nd,UserBasic[0].password_2nd)
        return result
    else:
        return False
        
        
    
def stock_line_chart():
    ValueSetting = value_setting.objects.defer("stock_value_now").all()[0]
    TrendRecord = trend_record.objects.all()
    ChartData = [["date",'单价']]

    for TRecord in TrendRecord:
        day = str(TRecord.day)[0:10]  
        _CharData = []
        _CharData.append(day)
        _CharData.append(float("%0.4f"%TRecord.value))
        ChartData.append(_CharData)
    NowData = []
    NowData.append(str(datetime.now()))
    NowData.append(float("%0.4f"%ValueSetting.stock_value_now))
    ChartData.append(NowData)
    result = json.dumps(ChartData)
    return result
    
    
    
    

def out_put_csv(request):
    """
    导出csv文件
    """
    from django.utils.http import urlquote
    now=datetime.now()
    s =""
    Result = request.session.get("Result")
    Content = request.session.get("Content")
    file_name = request.session.get('file_name',now)
    file_name = "".join(file_name.split(":"))
    response = HttpResponse(mimetype='text/csv')
    response.write('\xEF\xBB\xBF') 
    response['charset'] = 'utf-8'
    response['Content-Disposition'] = 'attachment; filename=%s.csv'% urlquote(file_name)
    writer = csv.writer(response)
    writer.writerow(Content)
    for r in Result:
        writer.writerow(r)
#        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    
    return response
    
#def out_put_csv(request):
#    """
#    导出csv文件
#    """
#    from django.utils.http import urlquote
#    now=datetime.now()
#    s =""
#    Result = request.session.get("Result")
#    Content = request.session.get("Content")
#    file_name = request.session.get('file_name',now)
#    file_name = "".join(file_name.split(":"))
#    response = HttpResponse(mimetype='text/ms-excel')
#    response.write('\xEF\xBB\xBF') 
#    response['Content-Disposition'] = 'attachment; filename=%s.xls'% urlquote(file_name)
#    writer = csv.writer(response)
#    writer.writerow(Content)
#    for r in Result:
#        writer.writerow(r)
##        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
#    return response
#    
def check_existing(request):    
    #如果调用Django的Field来处理会自动判断
    #常见的操作是用户上传图片后随机给一个名字
    #所以这里也可以直接返回0，即不存在
    return HttpResponse('0')
'''
用来处理的上传图片。如果这个函数独立存在的话，它的request.user
是匿名用户，request.session也和当前登录的用户不同。简单的解决
方法是接传入user_id
'''
from django.views.decorators.csrf import csrf_exempt
import os
import ImageFile  
@csrf_exempt
def upload_image(request,**kwargs): 
    image_url = ""
    file_ext = str(request.FILES['Filedata'].name).split('.')[-1]
#    ProductImage = product_image
    # 随机或者md5加密或者其他方式，让图片名字不重复
    time = str(datetime.now())
    file_name = time 
    user_upload_folder = os.path.join(settings.STATIC_ROOT,'images')
    if not os.path.exists(user_upload_folder):
        os.mkdir(user_upload_folder)
#    #这里是用二进制的方式操作，Django也提供了其他的方法
    file_upload = open( os.path.join(user_upload_folder, file_name+'.'+file_ext), 'w')

    file_upload.write(request.FILES['Filedata'].read())
    file_upload.close()
    return HttpResponse(file_name+'.'+file_ext)
def get_submmit_level(UserBasic=None):
    """
    获取用户的几星董事
    """
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT `V_SETTLE_CWEB_BASIC`.`level_name`,`V_SETTLE_CWEB_BASIC`.`threshold_value`,`V_SETTLE_CWEB_BASIC`.`gain_rate`,`V_SETTLE_CWEB_BASIC`.`is_summit` FROM `rtyk_triple`.`V_SETTLE_CWEB_BASIC` where id=%s',UserBasic.id)
        level = cursor.fetchall()[0]
        is_summit = level[3]
        UserBasic.mall_level = level[0]
        UserBasic.is_summit = is_summit
    except:
        is_summit = ''
    
    if is_summit:
        submmit_name = ['','一星董事','二星董事','三星董事','四星董事','五星董事','六星董事','七星董事']
        cursor.execute('SELECT FA_SUM.father_id as min_id , max(MA_SUM.id) as summit_level FROM (SELECT FATHER.id AS father_id , count(SON.id) AS summit_son_number FROM member_user_recommender AS RECC INNER JOIN member_user_basic AS FATHER ON FATHER.id = RECC.recommending_id INNER JOIN member_user_basic AS SON ON SON.id = RECC.recommended_id ,management_value_setting AS SETTING WHERE SON.mall_team_score > SETTING.grade_summit GROUP BY FATHER.id) AS FA_SUM INNER JOIN management_mall_summit AS MA_SUM ON FA_SUM.summit_son_number >= MA_SUM.summit_num where FA_SUM.father_id=%s GROUP BY min_id',UserBasic.id)
        
	try:
		submit = cursor.fetchall()[0]
        	UserBasic.mall_level = submmit_name[submit[1]]
	except:
		submit = ""
		UserBasic.mall_level = "";
    return UserBasic
