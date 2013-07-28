# -*- coding: utf8 -*-
import sys, threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.db.models import F, Q
from django.db.models import Count
from django.http import Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from decimal import *
import json
from datetime import *
import MySQLdb
import time
from TripleMag.apps.decorators import get_user_basic, admin_required, admin_or_store_required
from TripleMag.apps.member.models import *
from TripleMag.apps.mall.forms import ProductForm
from TripleMag.apps.management.forms import *
from TripleMag.apps.money.models import cash_withdraw, bonus_unpaid, bonus_declare_record, day_perform_record as day_perform_records, bonus_mall_record, store_declare_record
from TripleMag.apps.management.sql_view import WithDrawView
from TripleMag.apps.management.models import member_lv_money, file_upload, value_setting, mall_level, mall_summit
from TripleMag.apps.store.forms import AddressForm
from TripleMag.apps.store.models import stuff_type, stuff
from TripleMag.apps.views import CallProc, PaginatorFuc, stock_line_chart, out_put_csv
from TripleMag.apps.stock.models import selling_poll
from announcements.forms import AnnouncementAdminForm
from announcements.models import Announcement
from TripleMag.apps.stock.models import trend_record
from django.db import connection
from django.db import transaction
from django.utils.translation import ugettext_lazy as _, ugettext

from notification.models import *
from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@login_required
@admin_required
def index(request, **kwargs):
    """
    管理员界面各种首页
    """
    template_name = "management/base.html"
    notices = Notice.objects.notices_for(request.user, on_site=True, unseen=True)
    
    request.session['subject'] = ""
    ctx = {
        "notices": notices
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@admin_required
def member(request, **kwargs):
    """
    会员和报单中心管理首页
    """

    template_name = "management/member/base.html"
    """
    这里需要记录今天和昨天的操作记录
    包括用户的提现成功、会员的充值添加会员的记录、奖金发放记录、报单升级成功记录  
    """
#    return render_to_response(template_name,RequestContext(request,ctx))
    request.session['subject'] = 'manage_memeber'
    return render(request, template_name)
@login_required
@admin_required
def member_void(request, **kwargs):
    """
    空点会员列表
    """
    MemVoid = user_basic.objects.filter(is_void=True).order_by("-id")
    template_name = "management/member/member_void.html"
    MemVoid = PaginatorFuc(request, MemVoid, number=20)
    ctx = {
        "mem_void":MemVoid
    }
    return render_to_response(template_name, RequestContext(request, ctx))
@login_required
@admin_required
def sys_index(request, **kwargs):
    """
    系统设置首页
    """
    template_name = "management/sys/sys_base.html"
    ctx = {
        "h1":"欢迎来到系统设置首页"
    }
    request.session['subject'] = 'manage_sys'
    return render_to_response(template_name, RequestContext(request, ctx))


@login_required
@admin_required
def stock_index(request, **kwargs):
    """
    股票设置首页
    """
    from datetime import timedelta
    template_name = "management/stock/stock_base.html"
    request.session['subject'] = 'manage_stock'
    SellingPoll = selling_poll.objects.all().order_by("value")
    print SellingPoll
    
    ValueSetting = value_setting.objects.all()[0]
    TrendRecord = trend_record()
    stock_lock_form = StockLockForm
    stock_allotment_form = StockAllOtMentForm
    stock_value_form = StockSetValueForm
    stock_set_values_form = StockValuesForm
    call_proc = CallProc()
    cursor = connection.cursor()

    cursor.callproc("get_stock_statistics", ('', '', '', '',))
    cursor.execute('select @_get_stock_statistics_0')
    overall_total_count = cursor.fetchone()[0]

    cursor.execute('select @_get_stock_statistics_1')    
    today_total_count = cursor.fetchone()[0]
    
    cursor.execute('select @_get_stock_statistics_2')    
    total_stock_hold = cursor.fetchone()[0]
    
    cursor.execute('select @_get_stock_statistics_3')   
    total_distribution = cursor.fetchone()[0]
     
    ChartData = stock_line_chart()



    if request.method == "POST":
        
        if 'cancle' in request.POST: 
            ValueSetting.stock_lock_start = None
            stock_lock_form = StockLockForm
            ValueSetting.save()
        elif 'set' in request.POST:
            stock_lock_form = StockLockForm(request.POST)
            if stock_lock_form.is_valid():
                ValueSetting.stock_lock_start = stock_lock_form.cleaned_data['stock_lock_start']
                lock_days = stock_lock_form.cleaned_data['stock_lock_end'] - stock_lock_form.cleaned_data['stock_lock_start']
                ValueSetting.stock_locked_days = lock_days.days
                ValueSetting.save()
        elif 'stock_allotment' in request.POST:
            stock_allotment_form = StockAllOtMentForm(request.POST)                

            if stock_allotment_form.is_valid():
                rate = stock_allotment_form.cleaned_data['rate']
                
                proc_name = "stock_allotment"
                call_proc.CallProcFuc_1(proc_name, rate)
        elif 'stock_return_all' in request.POST:
            proc_name = "stock_return_all"
            call_proc.CallProcFuc_0(proc_name)
        elif 'set_stock_price' in request.POST:
            stock_value_form = StockSetValueForm(request.POST)
            if stock_value_form.is_valid():
                ValueSetting.stock_value_now = Decimal(stock_value_form.cleaned_data['stock_value_now'])
                ValueSetting.save()
        elif 'set_values' in request.POST:
            stock_set_values_form = StockValuesForm(request.POST, Value_Setting=ValueSetting)
            if stock_set_values_form.is_valid():
                print 'dghhh'
                stock_set_values_form.save()
                print 'sssssssssss'
    request.session['overall_total_count'] = overall_total_count
    if ValueSetting.stock_lock_start:
        stock_lock_start = ValueSetting.stock_lock_start
        stock_lock_end = stock_lock_start + timedelta(days=ValueSetting.stock_locked_days)
    else:
        stock_lock_start = None
        stock_lock_end = None
    
    ctx = {
        "stock_lock_form":stock_lock_form,
        "stock_lock_start": stock_lock_start,
        "stock_lock_end": stock_lock_end,
        "stock_allotment":stock_allotment_form,
        'stock_value_form':stock_value_form,
        'ValueSetting':ValueSetting,
        'stock_set_values_form':StockValuesForm,
        'ChartData':ChartData,
        'overall_total_count':overall_total_count,
        'today_total_count':today_total_count,
        'total_stock_hold':total_stock_hold,
        'total_distribution':total_distribution,
        "selling_poll":SellingPoll
    }
    cursor.close()
    connection.close()
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
def mall_index(request, **kwargs):
    """
    商城设置首页
    """
    template_name = 'management/mall/mall_base.html'
    ctx = {
        '':''
    }


    request.session['subject'] = 'manage_mall'
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required    
@admin_or_store_required
def add_member(request, **kwargs):
    """
    添加会员
    """
    template_name = kwargs.pop("template_name")
    role = kwargs.pop("role")
    ValueSetting = value_setting.objects.defer("password_1nd", "password_2nd").get(id=1)
    Level = member_lv_money.objects.all()
    Adding = kwargs.pop("Mem", None)
    error = ""
#    print roleUserBasic
    if request.method == "POST":
        basic_form = UserForm(request.POST, user=request.user)
        advanced_form = MemberForm(request.POST, user=request.user, role=request.POST.get("role"))
        address_form = AddressForm(request.POST)
        money_enough = True
        if basic_form.is_valid() and advanced_form.is_valid() and address_form.is_valid():
            try:
                _Level = Level.filter(level=advanced_form.cleaned_data['level'])[0]
            except:
                raise Http404
            if role == "MemMax":
                if Adding.store_order < _Level.money:
                    money_enough = False
                    error = "您的余额不足"
            if money_enough:
                user = User()
                username = basic_form.cleaned_data['number']
                password = basic_form.cleaned_data['password_1nd']
                email = ""
                #存储用户名和密码
                user = User.objects.create_user(username, email, password)

                UserBasic = user_basic(user=user, password_1nd=user.password)
                #存储用户的基本信息
                basic_form = UserForm(request.POST, user=request.user, instance=UserBasic)
                basic_form.password_1nd = user.password
                basic_form.save()
                UserAddress = user_address(user=UserBasic, is_primary=True)
                address = AddressForm(request.POST, instance=UserAddress)

    #            UserBasic.save()
                #存储推荐人
                recommending_number = basic_form.cleaned_data['recommending']
                if recommending_number:
                    UserRecommender = user_recommender()
                    UserRecommender.recommended = user_basic.objects.get(id=UserBasic.id)
                    UserRecommender.recommending = user_basic.objects.get(number=recommending_number)
                    UserRecommender.save()
                
    #            print basic_form.role
                
                #存储节点人
                contacting_number = advanced_form.cleaned_data['contacting']
                if contacting_number:
                    UserContactor = user_contactor()
                    UserContactor.contacted = UserBasic
                    UserContactor.contact_area = advanced_form.cleaned_data['contact_area']
                    UserContactor.contacting = user_basic.objects.get(number=contacting_number)
                    UserContactor.save()

                #存储会员信息
                
                
                UserMidMem = user_mid_mem()
                UserMidMem.user = UserBasic
                
                if not UserBasic.is_void:
                    UserMidMem.init_money = _Level.money
                else:
                    UserMidMem.init_money = 0
                UserMidMem.level = _Level
                address.save()
                try:
                    user.save()
                except:
                    ctx = {
                        'has_exit':"用户已经存在,请再选择一个",
                        'form': basic_form
                    }
                    return render_to_response(template_name, RequestContext(request, ctx))
                UserMidMem.save()
                if not UserBasic.is_void:
                    call_proc = CallProc()
                    call_proc.CallProcFuc_1("member_new", UserBasic.id)
                #存储报单中心信息
                if basic_form.cleaned_data['role'] == "MemMax":
                    UserMaxMan = user_max_mem()
                    UserMaxMan.user_mid = UserMidMem
                    if advanced_form.cleaned_data['style'] == '2':
                        UserMaxMan.is_central = True
                        UserMaxMan.save()
                    else:
                        UserMaxMan.is_central = False
    #                    UserCentralUsual =user_central_usual()
                        user_central = advanced_form.cleaned_data['user_central']
                        UserMaxMan.save()
                        if user_central:
                            UBasic = user_basic.objects.filter(number=user_central)[0]
                            user_mid = user_mid_mem.objects.get(user=UBasic)
                            UMax = user_max_mem.objects.filter(user_mid=user_mid)[0]
                            
                            user_central_usual.objects.create(user_central=UMax, user_usual=UserMaxMan)
                        
    #                UserMaxMan.save()

                #报单中心添加会员
                if role == "MemMax":
    #                try:
                    UserAdder = user_adder(adding=Adding, added=UserBasic)
                    Adding.store_order -= _Level.money
                    UMid = user_mid_mem.objects.get(user=Adding)
                    UserMaxMem = user_max_mem.objects.get(user_mid=UMid)
                    StoreDeclareRecord = store_declare_record(max=UserMaxMem, amount=_Level.money)
                    Adding.store_cash += _Level.money
                    StoreDeclareRecord.save()
                    Adding.save()
                    UserAdder.save()
                    return HttpResponseRedirect(reverse('store_index'))
                return HttpResponseRedirect(reverse('management_member_index'))
    else:
        basic_form = UserForm()
        advanced_form = MemberForm()
        address_form = AddressForm()
    ctx = {
        'basic_form': basic_form,
        'advanced_form': advanced_form,
        'UserAddressForm':address_form,
        'Level':Level,
        "password_1nd":ValueSetting.password_1nd,
        "password_2nd":ValueSetting.password_2nd,
        "error":error
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
@get_user_basic
def change_mem_info(request, **kwargs):
    """
    管理员修改会员的信息
    """
    
    
    

@login_required
@admin_required    
def search_member(request, **kwargs):
    """
    查询会员信息
    """
    #视图来实现，装饰器来判读用户身份输出相应的UserInfo
    query = request.GET.get("query", None)
    role = request.GET.get("role")
    current_role = "所有用户"
    if query:
        UserBasic = user_basic.objects.filter(Q(number__icontains=query) | Q(name__icontains=query)).order_by("-id")
    else:   
        UserBasic = user_basic.objects.all().order_by("-id")
    print role
    if role:
        if role == "MemMin":
            UserBasic = user_basic.objects.filter(Q(role__icontains="MemMin") | Q(role__icontains="MemVIP")).order_by("-id")
            current_role = "商城用户"
        elif role == "MemMax":
            current_role = "报单中心"
            UserBasic = user_basic.objects.filter(role__icontains=role).order_by("-id")
        elif role == "MemMid":
            current_role = "会员"        
            UserBasic = user_basic.objects.filter(role__icontains=role).order_by("-id")
    cursor = connection.cursor()  
    cursor.execute("select * from V_DELETABLE") 
    
    UserBasic.delete_able = False
    UserMidMem = user_mid_mem.objects.all()
    for UBasic in UserBasic:
        try:
            UMidMem = UserMidMem.get(user=UBasic)
            UBasic.level = UMidMem.level.name
        except:
            UBasic.level = "无"
    
    for row in cursor.fetchall():
        for u in UserBasic:
            if u.number == row[3]:
                u.delete_able = True

    if not request.is_ajax():
        template_name = "management/member/search_member.html"
    else:
        template_name = "management/member/user_info.html"
        
        
    UserBasic = PaginatorFuc(request, UserBasic, number=20)
    ctx = {
        'user_info':UserBasic,
        'role':role,
        'query':query,
        'current_role':current_role
    }

    return render_to_response (template_name, RequestContext(request, ctx))
    
@login_required
@admin_required

def delete_member(request, **kwargs):
    """
    删除会员
    """
    UserNumber = request.GET.get("user_number")

    UserBasic = user_basic.objects.defer("id").filter(number=UserNumber)
    print UserBasic[0].id
    cursor = connection.cursor()
    cursor.execute('delete from member_user_basic where id = %s', UserBasic[0].id)
#    print UserBasic
#    cursor.commit()
    connection.connection.commit()
    cursor.close()
    
    connection.close()
    return HttpResponseRedirect(reverse('management_search_member'))
    
@login_required    
@admin_required    
def add_product(request):
    """
    添加商品
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = ProductForm
    return render_to_response(
                                'management/add_product.html',
                                {'form':form},
                                context_instance=RequestContext(request)
                             )
@login_required       
@admin_required
@get_user_basic
def upgrade_appl_info(request, **kwargs):
    """
    查看报单中心申请
    """
    template_name = "management/member/upgrade_appl.html"
    UserAppl = member_mid_upgrade_record.objects.filter(state="wait").order_by("apply_time")
    
    ctx = {
        'user_appl': UserAppl
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
def application(request, **kwargs):
    """
    申请中心
    """
    template_name = "management/member/application.html"
    #信息修改申请
    UserModifyRecord = user_modify_record.objects.filter(state="wait").order_by('-time')
    
    #提现申请
    CashWithDraw = cash_withdraw.objects.filter(state="wait").order_by("-time_start")
    for c_withdraw in CashWithDraw:
        c_withdraw.amount = c_withdraw.amount
    #会员升级申请
    UserAppl = member_mid_upgrade_record.objects.filter(state="wait").order_by("apply_time")
    MinUpgradAppl = min_upgrade_record.objects.filter(state="wait").order_by("time")
    ctx = {
        'user_appl': UserAppl,
        "user_modify_record":UserModifyRecord,
        'withdraw_appl': CashWithDraw,
        'memmin_upgrade_appl':MinUpgradAppl
        
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@admin_required
def deal_memmin_upgrade_appl(request, **kwargs):
    """
    处理VIP升级申请
    """
    
    choice = request.GET.get("choice")
    appl_id = request.GET.get("appl_id")
    try:
        MinUpgradAppl = min_upgrade_record.objects.get(id=appl_id)
    except:
        raise Http404
    if choice == "allow":
        MinUpgradAppl.user.role = "MinVIP"
        MinUpgradAppl.user.bank_name = MinUpgradAppl.bank_name
        MinUpgradAppl.user.bank_account_id = MinUpgradAppl.bank_account_id
        MinUpgradAppl.user.bank_account_name = MinUpgradAppl.bank_account_name
        MinUpgradAppl.user.id_card_number = MinUpgradAppl.id_card_number
        MinUpgradAppl.state = "sure"
        MinUpgradAppl.user.save()
        extra_context = "恭喜你成为了商城VIP"
        notification.send(MinUpgradAppl.user.user, "vip_appl", extra_context, True, request.user)
    elif choice == "reject":
        MinUpgradAppl.state = "deny"
        extra_context = "很抱歉你的VIP申请被拒绝"
    notification.send(MinUpgradAppl.user.user, "vip_appl", extra_context, True, request.user)
    MinUpgradAppl.save()
    return HttpResponseRedirect(reverse("management_application"))
@login_required       
@admin_required
@get_user_basic
def allow_appl(request, **kwargs):
    """
    为会员开通申请
    """
    UserBasic = kwargs.pop("UserBasic")
    choice = request.GET.get("choice")
    UserAppl = member_mid_upgrade_record.objects.filter(user=UserBasic)[0]
#    try:
    if choice == "allow":

        store_style = request.GET.get("store_style")
        UserBasic.role = "MemMax"
        UserBasic.save()
        UserAppl.state = "sure"
        UserMidMem = user_mid_mem.objects.filter(user=UserBasic)[0]
        UserMaxMan = user_max_mem(user_mid=UserMidMem)

        if (store_style == "中心店"):
            UserMaxMan.is_central = True
        else:
            UserMaxMan.is_central = False

        UserMaxMan.save()
        extra_context = "你的报单中心已经开通，重新登录后即可生效"
    elif choice == "reject":
        UserAppl.state = "wait"
        extra_context = "你的报单中心申请失败"
    UserAppl.grant_time = datetime.datetime.now()

    UserAppl.save()
    notification.send(UserBasic.user, "store_appl_success_notice", extra_context, True, request.user)
    data = '1'
#    except:
#        data = '0'
    
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
@login_required           
@admin_required
@get_user_basic
def allow_or_reject(request, choices=None, user_number=None, **kwargs):
    """
    为会员开通或拒绝会员的报单中心申请
    """
    UserBasic = kwargs.pop("UserBasic")
    
    return HttpResponse("/")
    
@login_required               
@admin_required
def manage_stuff_type(request, **kwargs):
    """
    管理货物类型
    """
    StuffType = stuff_type.objects.all().order_by('-id')
    request.session['subject'] = "manage_stuff"
    template_name = 'management/member/manage_stuff_type.html'
    include_template = 'includes/stuff_type.html'
    StuffType = PaginatorFuc(request, StuffType)
    ctx = {
        "stuff_type": StuffType,
        'include_template': include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required                                    
@admin_required
def add_stuff_type(request, **kwargs):
    """
    添加货物类型
    """
    print 'ssss'
    template_name = 'management/member/manage_stuff_type.html'
    include_template = 'includes/add_stuff_type.html'
    
    if request.method == "POST":
        form = StuffTypeForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            success_url = reverse("manage_stuff_type")
            return HttpResponseRedirect(success_url)
    else:
        form = StuffTypeForm
    print form
    ctx = {
        'form': form,
        'include_template': include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required       
@admin_required
def del_stuff_type(request, **kwargs):
    """
    删除货物类型
    """
    stuff_type_id = request.GET.get('stuff_type_id', None)
    try:    
        StuffType = stuff_type.objects.get(id=stuff_type_id)
        StuffType.delete()
        data = '1'
    except:
        data = '0'
    return HttpResponse(json.dumps(data), mimetype="application/json")
@login_required       
@admin_required
def change_stuff_type(request, **kwargs):
    """
    修改货物类型信息
    """
    template_name = "management/member/change_stuff_type.html"

    if request.method == "POST":
        if 'change' in request.POST:
            StuffType = request.session.get('StuffType')
            name = request.POST.get('name')
            detail = request.POST.get('detail')
            picture = request.POST.get('picture')
            
            if name != StuffType.name:
                StuffType.name = name
            if detail != StuffType.detail:
                StuffType.detail = detail

            StuffType.save()
        success_url = reverse("manage_stuff_type")
        return HttpResponseRedirect(success_url)
    else:
        stuff_type_id = request.GET.get("stuff_type_id")
        
        try:
            stuff_type_id = int(stuff_type_id)
            
            StuffType = stuff_type.objects.get(id=stuff_type_id)
            
            request.session['StuffType'] = StuffType
            form = StuffType
        except:
            print '111111111'    
        
        print stuff_type_id
    ctx = {
        "StuffType":form
    }
    return render_to_response(template_name, RequestContext(request, ctx))
@admin_required
def manage_stuff(request, **kwargs):
    """
    管理货物
    """

    Stuff = stuff.objects.all().order_by('-id')
    
    template_name = 'management/member/manage_stuff_type.html'
    include_template = 'includes/stuff.html'
    Stuff = PaginatorFuc(request, Stuff)
    ctx = {
        "stuff": Stuff,
        'include_template': include_template
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
@admin_required
def add_stuff(request, **kwargs):
    """
    添加货物
    """
    template_name = "management/member/manage_stuff_type.html"
    include_template = "includes/add_stuff.html"
    
    if request.method == "POST":
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success_url = reverse("manage_stuff")
            return HttpResponseRedirect(success_url)
    else:
        form = StuffForm
        
    ctx = {
        'form':form,
        'include_template': include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@admin_required
def del_stuff(request, **kwargs):
    """
    删除货物
    """
    stuff_id = request.GET.get('stuff_id', None)
    try:    
        Stuff = stuff.objects.get(id=stuff_id)
        Stuff.delete()
        data = '1'
    except:
        data = '0'
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
@admin_required
def change_stuff(request, **kwargs):
    """
    修改货物
    """
    template_name = "management/member/change_stuff.html"

    if request.method == "POST":
        print 'ssss'
        Stuff = request.session.get('Stuff')
        name = request.POST.get('name')
        new_type = request.POST.get('type')
        total_num = request.POST.get('total_num')
        price_single = request.POST.get('price_single')
        detail = request.POST.get('detail')
        picture = request.POST.get('picture')
        if name != Stuff.name:
            print 'ssss', name
            Stuff.name = name
        if detail != Stuff.detail:
            Stuff.detail = detail
        if picture != Stuff.picture:
            Stuff.picture == picture
        if new_type != Stuff.type:
            StuffType = stuff_type.objects.get(id=new_type)
            Stuff.type = StuffType
        if total_num != Stuff.total_num:
            Stuff.total_num = total_num
            print total_num
        if price_single != Stuff.price_single:
            Stuff.price_single = price_single
        Stuff.save()
        
        success_url = reverse("manage_stuff")
        return HttpResponseRedirect(success_url)
        
    else:
        stuff_id = request.GET.get("stuff_id")

        try:
            stuff_id = int(stuff_id)
            StuffType = stuff_type.objects.all()
            Stuff = stuff.objects.get(id=stuff_id)
            request.session['Stuff'] = Stuff
        except:
            print '111111111'    
        ctx = {
            "Stuff": Stuff,
            "stuff_type": StuffType
        }
        return render_to_response(template_name, RequestContext(request, ctx))
@admin_required
@get_user_basic
def charge(request, user_number=None, **kwargs):
    """
    给会员充值
    """
    UserBasic = kwargs.pop("UserBasic")
    
    return render_to_response(
                        'management/charge.html',
                        {'UserBasic':UserBasic},
                        context_instance=RequestContext(request)
                      )
@admin_required
@get_user_basic            
def to_charge(request, **kwargs):
    """
    给会员充值 ajax
    """
    UserBasic = kwargs.pop("UserBasic")
    
    account = request.GET.get("account")
    amount = request.GET.get("amount")

    try:
        amount = Decimal(amount)
        if account == "cash":
            UserBasic.cash = UserBasic.cash + amount
            extra_context = "你的现金账户冲入" + str(amount) + "元"
            data = UserBasic.cash
            UserBasic.save()
            notification.send(UserBasic.user, "charge_notice", extra_context, True, request.user)

        elif account == "stock_hold":
            extra_context = "你的股票自有账户冲入" + str(amount) + "股"
            amount = int(amount)
            #调用存储过程函数
            call_proc = CallProc()
            call_proc.CallProcFuc_2("stock_recharge", UserBasic.id, amount)
            UBasic = user_basic.objects.get(id=UserBasic.id)
            data = UBasic.stock_hold_0devide + UBasic.stock_hold_1devide + UBasic.stock_hold_2devide
            notification.send(UserBasic.user, "charge_notice", extra_context, True, request.user)

        elif account == "store_order":
            extra_context = "你的报单账户账户冲入" + str(amount) + "元"
            UserBasic.store_order = UserBasic.store_order + amount
            data = UserBasic.store_order
            print data
            UserBasic.save()
            print data
            
            notification.send(UserBasic.user, "charge_notice", extra_context, True, request.user)
        elif account == "change_cash":
            UserBasic.cash = amount
            data = UserBasic.cash
            UserBasic.save()
        elif account == "stock_hold_0devide":
            
            UserBasic.stock_hold_0devide = amount
            print UserBasic.stock_hold_0devide
            UserBasic.save()
            data = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        elif account == "stock_hold_1devide":
            UserBasic.stock_hold_1devide = amount
            UserBasic.save()
            data = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        elif account == "stock_hold_2devide":
            UserBasic.stock_hold_2devide = amount
            UserBasic.save()
            data = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        elif account == "change_store_order":
            UserBasic.store_order = amount
            UserBasic.save()
            data = UserBasic.store_order
    except:
        data = '-1'
        extra_context = "充值失败"

    return HttpResponse(data, mimetype="application/json")
    
@admin_required 
def withdraw_appl(request, **kwargs):
    """
    查看会员的提现申请
    """
    template_name = "management/member/withdraw_appl.html"
    
    CashWithDraw = cash_withdraw.objects.filter(state="wait").order_by("-time_start")
    test = cash_withdraw.objects.all()

    ctx = {
        'withdraw_appl': CashWithDraw
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@admin_required
def deal_withdraw_appl(request, **kwargs):
    """
    处理会员的提现请求
    """ 
    choice = request.GET.get("choice")
    withdraw_id = request.GET.get("withdraw_id")
    CashWithDraw = cash_withdraw.objects.get(id=withdraw_id)
    
    try:
        if choice == "允许":
            CashWithDraw.state = "sure"
            CashWithDraw.time_authorize = datetime.datetime.now()
            CashWithDraw.save()
            
            extra_context = "提现成功"
            label = "withdraw_success_notice"
        elif choice == "拒绝":
            
            CashWithDraw.user.cash = CashWithDraw.user.cash + CashWithDraw.amount
            CashWithDraw.time_authorize = datetime.datetime.now()
            CashWithDraw.user.save()
            CashWithDraw.state = "deny"
            CashWithDraw.save()
            extra_context = "提现被拒绝"
            label = "withdraw_failed_notice"
        notification.send(CashWithDraw.user.user, label , extra_context, True, request.user)
        data = '1'
    except:
        data = '0'
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
@admin_required
def withdraw_record(request, querys=None, **kwargs):
    """
    用户的提现记录
    """
    try:
        query = querys.split("_")
    except:
        query = ["all"]
    query_result = {
        "number": WithDrawView.objects.get(number__contains=query[1]),
        "name": WithDrawView.objects.filter(name__contains=query[1]),
        "time_start": WithDrawView.objects.filter(time_start_range(query[1], query[2])),
        "time_authorize": WithDrawView.objects.filter(time_authorize_rang(query[1], query[2])),
        "state": WithDrawView.objects.filter(state=query[1]),
        "all": WithDrawView.objects.all()
    }
    
    try:
        query_result[query[0]]
    except:
        print 'wrong'
    return HttpResponse('/')
            
@admin_required
def mem_appl_manage(request):
    """
    会员信息申请管理
    """
    template_name = "management/mem_appl_manage.html"
    
    UserModifyRecord = user_modify_record.objects.filter(state="wait").order_by['-time']
    
    ctx = {
        "user_modify_record":UserModifyRecord
    }
    return render_to_response(template, RequestContext(request, ctx))
    
@admin_required   
def del_appl(request, **kwargs):
    """
    处理用户的请求
    """
    record_id = request.GET.get('record_id')
    choice = request.GET.get("choice")
    UserModifyRecord = user_modify_record.objects.get(id=record_id)
    print UserModifyRecord.state
#        except:
#            data = '1'
#        extra_context = "信息修改成功"
#        notification.send(UserBasic.user, "change_info_success_notice",extra_context,True, request.user)
        
#    def reject_fuc(UserModifyRecord,UserBasic):
    print choice
        
    if choice == "allow":
        if UserModifyRecord.name:
            print '1'
            UserModifyRecord.user.name = UserModifyRecord.name
        if UserModifyRecord.bank_name:
            print '2'
            UserModifyRecord.user.bank_name = UserModifyRecord.bank_name
        if UserModifyRecord.bank_account_id:
            UserModifyRecord.user.bank_account_id = UserModifyRecord.bank_account_id 
        if UserModifyRecord.bank_account_name:
            print '4'
            UserModifyRecord.user.bank_account_name = UserModifyRecord.bank_account_name
        if UserModifyRecord.id_card_num:
            UserModifyRecord.user.id_card_number = UserModifyRecord.id_card_num
        UserModifyRecord.state = "sure"
        UserModifyRecord.save()
        UserModifyRecord.user.save()
        extra_context = "信息修改成功"
        data = '1'
    elif choice == "reject":
        print 'lllk'
        UserModifyRecord.state = "deny"
        UserModifyRecord.save()
        extra_context = "信息修改被拒绝"
        
        data = '1'
    notification.send(UserModifyRecord.user.user, "change_info_failed_notice", extra_context, True, request.user)
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
@admin_required
@get_user_basic    
def change_state(request, **kwargs):
    """
    对用户的状态进行修改
    """    
    UserBasic = kwargs.pop("UserBasic")
    choice = request.GET.get('choice')
    try:
        if choice == 'stock_0':
            UserBasic.is_stock_XR = False
            extra_context = "股票解除除权"
            label = "stock_is_not_xr_notice"
            
        elif choice == 'stock_1':
            UserBasic.is_stock_XR = True
            extra_context = "股票被除权"
            label = "stock_is_xr_notice"
            
        elif choice == 'block_0':
            UserBasic.is_blocked = False
            extra_context = "账户解除冻结"
            label = "is_blocked_notice"
            
        elif choice == 'block_1':
            UserBasic.is_blocked = True
            extra_context = "账户被冻结"
            label = "not_blocked_notice"
        UserBasic.save()
        notification.send(UserBasic.user, label , extra_context, True, request.user)
        data = '1'
    except:
        data = '0'
    return HttpResponse(json.dumps('1'), mimetype="application/json")
    
@admin_required   
def charge(request, **kwargs):
    """
    给用户的账户进行充值 
    """
    query = request.GET.get("query", None)
    if query:
        template_name = "management/member/charge_user_info.html"
        UserBasic = user_basic.objects.filter(Q(number__contains=query) | Q(name__contains=query))

    else:
        template_name = "management/member/charge.html" 
        UserBasic = None
        
    ctx = {
        'user_basic': UserBasic
    }  
    
    return render_to_response(template_name, RequestContext(request, ctx))

@admin_required
def bank_info(request, **kwargs):
    """
    查看会员的账户信息
    """
    query = request.GET.get("query", None)
    if query:
        template_name = "management/member/bank_info_table.html"
        UserBasic = user_basic.objects.filter(Q(number__contains=query) | Q(name__contains=query))

    else:
        template_name = "management/member/bank_info.html" 
        UserBasic = user_basic.objects.all()
        
    ctx = {
        'bank_info': UserBasic
    }  
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
@admin_required
def upload_file(request, **kwargs):
    """
    资料上传
    """
    template_name = "management/sys/file_upload.html"
    
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('management_file_list'))
    else:
        form = FileUploadForm
    
    ctx = {
        "form": form
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
def public_announcements(request, **kwargs):
    """
    发布公告
    """
    template_name = "announcements/public_announcement.html"
    user = request.user
    if request.method == "POST":
        announcement = Announcement(creator=user, members_only=True)
        form = AnnouncementAdminForm(request.POST, instance=announcement)

        if form.is_valid():
            form.save()
            extra_context = "有新的公司公告"
            users = User.objects.exclude(id=request.user.id)
            notification.send(users, "announcement_notice", extra_context, True, request.user)
            return HttpResponseRedirect(reverse("announcements_list"))
    else:
        form = AnnouncementAdminForm
        
    ctx = {
        "form": form
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))    
        
def announcements_list(request, **kwargs):
    """
    查看公告列表
    """
    announcement_id = request.GET.get("announcement_id")

    if announcement_id == None:
        template_name = kwargs.pop("template_name")
        announcements = Announcement.objects.all().order_by("-creation_date")
        ctx = {
        "announcements": announcements,
        'role': request.session.get('role')
            }
    else:
        template_name = "announcements/announcement_detail.html"
        announcements = Announcement.objects.get(id=announcement_id)
        print announcements
        ctx = {
            "announcements": announcements
        }
    print template_name
    return render_to_response(template_name, RequestContext(request, ctx))

#@login_required
#@admin_required
#def a_bonus_settlement(request ,**kwargs): 
#    """
#    A网奖金结算
#    """   
#    proc_name = "settle_account"
#    call_proc = CallProc()
#    call_proc.CallProcFuc_0(proc_name)

#    goto_url = reverse("a_bonuses")
#    return HttpResponseRedirect(goto_url)

#@login_required
#@admin_required
#def a_bonuses(request, **kwargs):
#    """
#    A网奖金发放
#    """
#    template_name = "management/member/a_bonuses.html"
#    if request.method == "POST":
#        try:
#            proc_name = "PAY_AWEB"
#            call_proc = CallProc()
#            call_proc.CallProcFuc_0(proc_name)
#            result = "结算成功"
#            HttpResponseRedirect(reverse('management_member'))
#        except:
#            result = "结算失败"
        
#    return render_to_response(template_name, RequestContext(request ,ctx))
@login_required
@admin_required
def a_bonus_settlement(request , **kwargs): 
    """
    A网奖金结算
    """   
    proc_name = "settle_account"
    call_proc = CallProc()
    call_proc.CallProcFuc_0(proc_name)

    goto_url = reverse("function_switch")
    return HttpResponseRedirect(goto_url)
@login_required
@admin_required
def c_bonus_settlement(request, **kwargs):
    """
    C网奖金结算和发放
    """
    proc_name = "pay_cweb"
    call_proc = CallProc()
    call_proc.CallProcFuc_0(proc_name)
    goto_url = reverse("function_switch")
    return HttpResponseRedirect(goto_url)
#@login_required
#@admin_required
#def c_bonuses(request, **kwargs):
#    """
#    C网奖金发放
#    """

#    if request.method == "POST":
#        try:
#            proc_name = "PAY_CWEB"
#            call_proc = CallProc()
#            call_proc.CallProcFuc_0(proc_name)
#            result = "结算成功"
#            HttpResponseRedirect(reverse('management_member'))
#        except:
#            result = "结算失败"
#        

#    return render_to_response(template_name, RequestContext(request ,ctx))

def a_bonus_counter(request, **kwargs):
    """
    每期的奖金记录
    """
    
    Counter = None
    counter = request.GET.get('counter', None)
    bonus_style = kwargs.pop("bonus_style")
    if request.is_ajax() :

        if bonus_style == "a_bonus":
            template_name = "includes/counter_detail.html"
            BonusRecords = bonus_declare_record.objects.filter(counter=counter).order_by("-id")
            csv_fuc(request, BonusRecords)
        elif bonus_style == "c_bonus":
            template_name = "includes/c_counter_detail.html"
            BonusRecords = bonus_mall_record.objects.filter(counter=counter).order_by("-id")
            csv_fuc_c(request, BonusRecords)
        BonusRecords = PaginatorFuc(request, BonusRecords, number=20)
        ctx = {
            'BonusRecords':BonusRecords,
            'counter':counter
        }
        return render_to_response(template_name, RequestContext(request, ctx))
#        template_name = "includes/counter_detail.html"
#        template_name = request.GET.get("template_name")
    else:
        template_name = 'management/member/a_bonus_counter.html'
        if bonus_style == "a_bonus":
            Counter = bonus_declare_record.objects.values('counter').annotate(Count('counter')).order_by("-counter")
            include_template = 'includes/counter_detail.html'
            Counter = PaginatorFuc(request, Counter)
            try:
                counter = Counter[0]['counter']
            except:
                counter = 0
            BonusRecords = bonus_declare_record.objects.filter(counter=counter).order_by("-id")
            csv_fuc(request, BonusRecords)
        elif bonus_style == "c_bonus":
            Counter = bonus_mall_record.objects.values('counter').annotate(Count('counter')).order_by("-counter")
            include_template = 'includes/c_counter_detail.html'
            Counter = PaginatorFuc(request, Counter)
            try:
                counter = Counter[0]['counter']
            except:
                counter = 0
            BonusRecords = bonus_mall_record.objects.filter(counter=counter).order_by("-id")
            csv_fuc_c(request, BonusRecords)
            
        BonusRecords = PaginatorFuc(request, BonusRecords, number=20)
#    detail_paginator = Paginator(BonusRecords, 10)
#    try:
#        detail_page = int(request.GET.get('detail_page', '1'))
#    except ValueError:
#        detail_page = 1 
#    try:
#        BonusRecords = detail_paginator.page(detail_page)
#    except (EmptyPage, InvalidPage):
#        BonusRecords = detail_paginator.page(detail_paginator.num_pages)
#    
    if not Counter:
        ctx = {
        "BonusRecords": BonusRecords,
        "counter": counter,
        'include_template':include_template
        }
    else:
        ctx = {
        "BonusRecords": BonusRecords,
        "counter": counter,
        "Counters": Counter,
        'include_template':include_template
        }
    return render_to_response(template_name, RequestContext(request, ctx))

def csv_fuc(request, BonusRecords):
    """
    CSV文件导出函数
    """
    Content = ['期数', '用户编号', '用户姓名', '报单费', '组织奖', '回本奖', '互助奖', '抽税', '重复消费', '到账统计', '奖金发放时间']
    Result = []
    counter = 0
    for R in BonusRecords:
        result = []
        number = ""
        name = ""
        try:
            number = R.mid.user.number
            print number
        except:
            print number
        try:
            name = R.mid.user.name
        except:
            print name
        result.append(R.counter)
        result.append(number)
        result.append(name)
        result.append(R.bonus_declare)
        result.append(R.bonus_group)
        result.append(R.bonus_recost)
        result.append(R.bonus_comhelp)    
        result.append(R.tax)
        result.append(R.bonus_repeat)
        result.append(R.total)
        try:
            result.append(R.time.strftime("%Y.%m.%d"))
        except:
            result.append("--")
        Result.append(result)
        counter = R.counter
    if request.user.is_superuser:
        file_name = "第%s期A网奖金记录" % (str(counter))
    else:
        now = datetime.datetime.now()
        file_name = "第A网奖金记录%s" % (str(now))
    request.session['Content'] = Content
    request.session['Result'] = Result
    request.session['file_name'] = file_name
def csv_fuc_c(request, BonusRecords):
    """
    C网奖金记录
    """
    Content = ['用户编号', '用户姓名', '零售奖', '同级奖', '推荐奖', '代理奖', '抽税', '到账总计', '奖金发放时间']
    Result = []
    counter = 0
    number = ""
    name = ""
    for R in BonusRecords:
        result = []

        try:
            number = R.user.number
        except:
            print number
        try:
            name = R.user.name
        except:
            print name
        result.append(number)
        result.append(name)  
        result.append(R.bonus_retail) 
        result.append(R.bonus_summit)
        result.append(R.bonus_recommend)
        result.append(R.bonus_proxy)
        result.append(R.tax)
        result.append(R.total)
        result.append(R.time.strftime("%Y.%m.%d"))
        counter = R.counter
        Result.append(result)
    if request.user.is_superuser:
        file_name = "第%s期C网奖金记录" % (str(counter))
    else:
        now = datetime.datetime.now()
        file_name = "第C网奖金记录%s" % (str(now))
    request.session['Content'] = Content
    request.session['Result'] = Result
    request.session['file_name'] = file_name
@login_required
@admin_required
def counter_detail(request , **kwargs):
    """
    每期奖金明细
    """
    template_name = "includes/counter_detail.html"
    Counter = kwargs.pop("counter")
    CounterDetail = bonus_declare_record.objects.filter(counter=Counter).order_by("-id")
    
@admin_required
def bonus_detail(request, **kwargs):
    """
    奖金发放 
    """
    BonusDetail = bonus_unpaid.objects.filter(paid=False)
    template_name = "management/member/bonus_detail.html"
    ctx = {
        "BonusDetails":BonusDetail
    }
    return render_to_response(template_name, RequestContext(request, ctx))
@login_required
@get_user_basic
def day_perform_record(request, **kwargs):
    """
    每天的业绩累计
    """
    template_name = kwargs.pop("template_name")
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    if request.user.is_superuser:
        if start_time:
            if not end_time:
                DayPerformRecord = day_perform_records.objects.filter(date__gte=start_time).order_by("-date").order_by("-date")
            else:
                DayPerformRecord = day_perform_records.objects.filter(date__range=(start_time, end_time)).order_by("-date").order_by("-date")
        else:
            DayPerformRecord = day_perform_records.objects.all().order_by("-date")
    else:
        if start_time:
            DayPerformRecord = day_perform_records.objects.filter(date__range=(start_time, end_time)).order_by("-date").order_by("-date")
        else:
            UserBasic = user_basic.objects.defer(None).filter(user=request.user)[0]
            UserMidMem = user_mid_mem.objects.filter(user=UserBasic)[0]
            DayPerformRecord = day_perform_records.objects.filter(mid=UserMidMem)
    Result = []
    request.session['Content'] = ['编号', '姓名', '日期', 'A区业绩值', 'B区业绩值']
    for R in DayPerformRecord:
        result = []
        result.append(R.mid.user.number)
        result.append(R.mid.user.name)
        result.append(R.date.strftime("%Y.%m.%d"))
        result.append(R.accumulate_a)
        result.append(R.accumulate_b)
#        result.append(R.accumulate_self)
        Result.append(result)
    request.session['Result'] = Result
    request.session['file_name'] = "每日报单值"
    DayPerformRecord = PaginatorFuc(request, DayPerformRecord)
        
    ctx = {
        "day_perform_record": DayPerformRecord,
        "start_time":start_time,
        "end_time":end_time,
        "out_put_name":"每日业绩导出"
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
def recommender(request, **kwargs):
    """
    管理员查看3代推荐人
    """
    user = request.user
    UserBasic = user_basic.objects.defer('id', "name", "number").all()
    user_number = request.GET.get("user_number")
    recommender_first = {}
    recommender_second = {}
    recommender_third = {}
    recommender_list = {}
    UBasic = ""

    
    cursor = connection.cursor()
    if user.is_superuser or user.first_name == "finance":
        UBasic = UserBasic.filter(number=user_number)[0]
        template_name = "management/member/recommender.html"
    else:
        UBasic = UserBasic.filter(user=user)[0]
        template_name = "member/recommender.html"
    request.session['recommender_name'] = UBasic.name
#        cursor.execute("select * from V_REC_GEN3 where  = %s",UBasic.id)
    #第一代推荐人关系
    UserRecommender = user_recommender.objects.filter(recommending=UBasic)
    #第二代推荐人关系
    
    for URecommender in UserRecommender:
        print URecommender.recommended.id, 'test'
        cursor.execute("select * from V_REC_GEN2 where son = %s", URecommender.recommended.id)
        result = cursor.fetchall()
#        cursor.close()
#        connection.close()
        print result
        for r in result:
            _recommender_second = {}
            try:
                _recommender_second['father'] = UserBasic.get(id=r[1])
            except:
                _recommender_second['father'] = None
            try:
                _recommender_second['son'] = UserBasic.get(id=r[2])
            except:
                _recommender_second['son'] = None
            cursor.execute("select * from V_REC_GEN3 where grandson = %s", r[2])
            _result = cursor.fetchall()
            for _r in _result:

                _recommender_third = {}
                try:
                    _recommender_third['father'] = UserBasic.get(id=_r[2])
                except:
                    _recommender_third['father'] = None
                try:
                    _recommender_third['son'] = UserBasic.get(id=_r[3])
                except:
                    _recommender_third['son'] = None
                recommender_third[_r] = _recommender_third
            recommender_second[r] = _recommender_second
        recommender_first[URecommender] = URecommender
    cursor.close()
    connection.close()
#    recommender = user_recommender.objects.filter(recommending = UserBasic)
#    user_detail = UserBasic.number
#    recommender_list = []
    
#    recommender_list = recommender_display(recommender,3)
    ctx = {
        "recommender_first":recommender_first,
        "recommender_second":recommender_second,
        "recommender_third":recommender_third,
        "UserBasic":UBasic
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
#def recommender_display(recommender,i):
#    """
#    递归函数
#    """
#    display_list = []
#    
#    if i==0:
#        print '11'
#    else:
#        i = i-1

#        for Recommended in recommender:
#            UserBasic = Recommended.recommended
#            user_detail = UserBasic.number
#            display_list.append(user_detail)        
#            recommender = user_recommender.objects.filter(recommending = UserBasic )
#            if recommender:
#                display_list.append(recommender_display(recommender,i))
#    return display_list


@login_required
@get_user_basic        
def a_bonus_detail(request, **kwargs):
    """
    奖金明细表
    """ 
    template_name = kwargs.pop("template_name")
    UserBasic = kwargs.pop("UserBasic")
    bonus_style = kwargs.pop("bonus_style")
    _paid = request.GET.get("paid", 0)
    paid = False
    if _paid == '0':
        print _paid, 'dddd'
        paid = False
    elif _paid == '1':
        print _paid, 'dddd'
        paid = True
    sub_website = kwargs.pop("sub_website", "")
    if request.method == "POST":
        if bonus_style == "a_bonus":
            try:
                proc_name = "PAY_AWEB"
                call_proc = CallProc()
                call_proc.CallProcFuc_0(proc_name)
                result = "结算成功"
                HttpResponseRedirect(reverse('management_member_index'))
            except:
                result = "结算失败"
        if bonus_style == "c_bonus":
#            try:
            proc_name = "pay_cweb"
            call_proc = CallProc()
            print proc_name, 'test'
            call_proc.CallProcFuc_0(proc_name)
            result = "结算成功"
            print result 
            HttpResponseRedirect(reverse('management_member_index'))
#            except:
            result = "结算失败"
    if request.user.is_superuser or request.user.first_name == "finance":
        if bonus_style == "a_bonus":
            BonusDetail = bonus_unpaid.objects.filter(type__in=['comhelp', 'recost', 'declare', 'group'], paid=paid).order_by("-id")
            csv_a_detail(request, BonusDetail, file_name="产品销售奖金明细")
        elif bonus_style == "c_bonus":
            BonusDetail = bonus_unpaid.objects.filter(type__in=['retail', 'summit', 'recommend', 'agent'], paid=paid).order_by("-id")
            csv_a_detail(request, BonusDetail, file_name="商城奖金明细")
    else:
        UserBasic = user_basic.objects.filter(user=request.user)[0]
        if bonus_style == "a_bonus":
            BonusDetail = bonus_unpaid.objects.filter(to_user=UserBasic, type__in=['comhelp', 'recost', 'declare', 'group'], paid=paid).order_by("-id")
            csv_a_detail(request, BonusDetail, file_name="产品销售奖金明细")
        elif bonus_style == 'c_bonus':
            BonusDetail = bonus_unpaid.objects.filter(type__in=['retail', 'summit', 'recommend', 'agent'], to_user=UserBasic, paid=paid).order_by("-id")
            csv_a_detail(request, BonusDetail, file_name="商城奖金明细")
    BonusDetail = PaginatorFuc(request, BonusDetail, number=20)
    ctx = {
        "BonusDetails": BonusDetail,
        'UserBasic': UserBasic,
        'sub_website':sub_website,
        'bonus_style':bonus_style,
        'paid':paid
    }
    return render_to_response(template_name, RequestContext(request, ctx))

def csv_a_detail(request, BonusDetail, file_name=None):
    """
    奖金明细文件导出
    """
    Content = ['用户编号', "用户姓名", '奖金类型', '奖金数额', '触发奖金用户编号', '触发奖金用户姓名', '奖金是否发放', '奖金发放时间']
    Result = []
    name = ""
    number = ""
    for R in BonusDetail:
        result = []
        try:
            number = R.to_user.number
        except:
            number = "***"
        try:
            name = R.to_user.name
        except:
            name = "***"
        result.append(number)
        result.append(name)
        result.append(R.get_type_display())
        result.append(R.amount)
        result.append(R.cause_user.number)
        result.append(R.cause_user.name)
        if R.paid:
            result.append("已经发放")
        else:
            result.append("未发放")
        try:
            result.append(R.time.strftime("%Y.%m.%d"))
        except:
            result.append("--")
        Result.append(result)
    
    file_name = file_name + str(datetime.datetime.now())
    request.session['file_name'] = file_name
    request.session['Content'] = Content
    request.session['Result'] = Result

@login_required
@admin_required
def function_switch(request, **kwargs):
    """
    功能开关
    """
    error = request.GET.get("warnings", "")
    print error
    password_form = Password1stForm()
    ValueSetting = value_setting.objects.defer("switch_member_login", 'switch_stock',
                                                'switch_store_declare', 'switch_mall', 'switch_mall_sign_in').get(id=1)
    function_choose = request.GET.get('function_choose', None)

    if function_choose:
        if function_choose == "switch_member_login_f":
            ValueSetting.switch_member_login = False
        elif function_choose == "switch_stock_f":
            ValueSetting.switch_stock = False
        elif function_choose == "switch_stock_t":
            ValueSetting.switch_stock = True
        elif function_choose == "switch_member_login_t":
            ValueSetting.switch_member_login = True
        elif function_choose == "switch_store_declare_f":
            ValueSetting.switch_store_declare = False
        elif function_choose == "switch_store_declare_t":
            ValueSetting.switch_store_declare = True
        elif function_choose == "switch_mall_f":
            ValueSetting.switch_mall = False
        elif function_choose == "switch_mall_t":
            ValueSetting.switch_mall = True
        elif function_choose == "switch_mall_sign_in_f":
            ValueSetting.switch_mall_sign_in = False
        elif function_choose == "switch_mall_sign_in_t":
            ValueSetting.switch_mall_sign_in = True
        
        ValueSetting.save()
    template_name = 'management/sys/function_switch.html'
    ctx = {
        'ValueSetting':ValueSetting,
        "error":error,
        'password_form':password_form
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@admin_required
def a_web_value_setting(request, **kwargs):
    """
    A网数值设定
    """
    
    template_name = "management/sys/a_web_value_setting.html"
    ValueSetting = value_setting.objects.defer("password_1nd", 'password_2nd', 'withdraw_rate', 'declare_central_rate',
                                                'declare_normal_rate', 'bonus_tax_rate', 'repo_rate', 'recost_rate',
                                                'comhelp_rate', 'comhelp_1st_min', 'comhelp_2nd_min',
                                                'comhelp_3rd_min',).get(id=1)
    MemberLvMoney = member_lv_money.objects.all()
    
    if request.method == "POST":
        a_web_value_setting_form = AWebValueSettingForm(request.POST, ValueSetting=ValueSetting)
        Money = request.POST.getlist("money", None)
        DayMax = request.POST.getlist("day_max", None)
        LowPercentage = request.POST.getlist("low_percentage", None)
        i = 0
        for MLvMoney in MemberLvMoney:
            MLvMoney.money = Money[i]
            MLvMoney.day_max = DayMax[i]
            MLvMoney.low_percentage = LowPercentage[i]        
            i += 1
            MLvMoney.save()
        if a_web_value_setting_form.is_valid():
            return HttpResponseRedirect(reverse("a_web_value_setting"))
    else:
        a_web_value_setting_form = AWebValueSettingForm()
    
    ctx = {
        'MemberLvMoney':MemberLvMoney,
        'ValueSetting':ValueSetting
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    #--------------------------
    #Function switch
@login_required
@admin_required
def c_web_value_setting(request, **kwargs):
    """
    C网数值设定
    """
    #运输方式和费用的json文件
    trans_expenses = ""
    ValueSetting = value_setting.objects.defer("grade_summit", 'mall_VIP_threshold', 'mall_love_rate', 'mall_car_rate',
                                                'mall_house_rate', 'mall_travel_rate', 'mall_share_rate',
                                                'mall_proxy_rate', 'mall_recommend_rate', 'mall_proxy_prov',
                                                'mall_proxy_city', 'mall_proxy_area', 'mall_tax_rate').get(id=1)
                                                
    management_mall_level = mall_level.objects.all()
    management_mall_summit = mall_summit.objects.all()
#    with open('/home/hump/TripleMag-env/TripleMag/TripleMag/static/js/transportation_expenses.json','r') as f:
#        trans_expenses = json.load(f)     
    with open('/home/rtyk/webapps/triple_mag/TripleMag/TripleMag/static/js/transportation_expenses.json', 'r') as f:
        trans_expenses = json.load(f)     
#    
#    f = json.loads(open("/home/hump/TripleMag-env/TripleMag/TripleMag/static/js/transportation_expenses.json"))
#    data = f.read()
#    print data
    if request.method == "POST":
        c_web_value_setting_form = CWebValueSettingForm(request.POST, ValueSetting=ValueSetting)
        MinScore = request.POST.getlist("min_score", None)
        MaxScore = request.POST.getlist("max_score", None)
        TresholdValue = request.POST.getlist("threshold_value", None)
        GainRate = request.POST.getlist("gain_rate", None)
        SummitNum = request.POST.getlist("summit_num", None)
        print SummitNum
        DayMax = request.POST.getlist("day_max", None)
        print DayMax, 'thsss'
        i = 0
        for MallLevel in management_mall_level:
            MallLevel.min_score = MinScore[i]
            MallLevel.max_score = MaxScore[i]
            MallLevel.threshold_value = TresholdValue[i]
            MallLevel.gain_rate = GainRate[i]
            i += 1
            MallLevel.save()
        i = 0
        for MallSummit in management_mall_summit:
            MallSummit.summit_num = SummitNum[i]
            MallSummit.bonus_percent = DayMax[i]
            print DayMax[i]
            i += 1
            MallSummit.save()
        if c_web_value_setting_form.is_valid():
            return HttpResponseRedirect(reverse("c_web_value_setting"))
    else:
        c_web_value_setting_form = CWebValueSettingForm()
        
        
    template_name = "management/sys/c_web_value_setting.html"
    ctx = {
        'ValueSetting':ValueSetting,
        "management_mall_level":management_mall_level,
        "management_mall_summit":management_mall_summit,
        "trans_expense":trans_expenses
        
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@admin_required
def contacting_chart(request, **kwargs):
    """
    查看接点人的业绩图
    """
    user_id = request.GET.get("user_id")
    user_number = request.GET.get("user_number")
    UBasic = user_basic.objects.defer("name", 'is_void').all()
    if user_id:
        try:
            UserBasic = UBasic.get(id=user_id)
        except:
            raise Http404
    if user_number:
        try:
            UserBasic = UBasic.get(number=user_number)
            user_id = UserBasic.id
        except:
            raise Http404
    request.session['contactor_name'] = UserBasic.name
    call_proc = CallProc()
    cursor = connection.cursor()
    template_name = "management/member/conactor.html"
    proc_name = "get_contactor_information"
    call_proc.CallProcFuc_1(proc_name, user_id)
    chart_data = "["
    cursor.execute('select * from t_cont_info')
    result = cursor.fetchall()
    print result
    c = range(1000)
    if result:
        father_number = None
        for r in result:
            
            my_id = int(r[0])
            _UserBasic = UBasic.get(id=my_id)
            
            try:
                father_id = int(r[1])
            except:
                father_id = None
            _data = ""
            _data += "[{v:\'" + str(r[2]) + "\', f: \'" + str(r[4]) + "<br /><a href=\"/management/contacting_chart/?user_id=" + str(r[0]) + "\">" + str(r[2])
            if _UserBasic.is_void:
                _data += "</a><br />空点会员"

            _data += "</a><br />A区<b class=\"color_em_purple\">" + str(r[5])
            _data += "</b>|B区<b class=\"color_em_purple\">" + str(r[6]) + "</b><br />总业绩<b class=\"color_em_purple\">" + str(r[7]) + "</b>"

            _data += "<br />" + str(r[8]) + "级代理'},"
            try:
                father_number = c[father_id]
                _data += "\'" + father_number + "\',\'" + str(r[3]) + "区\'],"
            except:
                _data += "\'\',\'" + str(r[3]) + "区\'],"
            c[my_id] = r[2]
            chart_data += _data
#    chart_data = chart_data[:-1]

    chart_data += "]"
    print chart_data
    ctx = {
        "chart_data":chart_data
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
def clean_data(request, **kwargs):
    """
    清空数据
    """
    password_1st = request.POST.get("password_1st")
    user = request.user
    password_form = Password1stForm(request.POST, user=user)
    if password_form.is_valid():
        proc_name = "Reset_all"
        call_proc = CallProc()
        call_proc.CallProcFuc_0(proc_name)
        url = reverse("function_switch") + "?warnings=清空数据成功"
        return HttpResponseRedirect(url)
    ctx = {
        'password_form':password_form
    }
    template_name = 'management/sys/function_switch.html'
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@admin_required
def make_day_check(request, **kwargs):
    """
    模拟过了一日
    """
    call_proc = CallProc()
    proc_name = "everyday_check"
    call_proc.CallProcFuc_0(proc_name)
    return HttpResponseRedirect(reverse("function_switch"))
@login_required
@admin_required
def test_data(request, **kwargs):
    """
    测试数据
    """
    call_proc = CallProc()
    proc_name = "StartupTester"
    call_proc.CallProcFuc_0(proc_name)
    return HttpResponseRedirect(reverse("function_switch"))

@login_required
@admin_required
def manage_announcement(request, **kwargs):
    """
    删除公司公告
    """
    from announcements.models import Announcement

    if request.method == "POST":
        announcement = request.session.get('announcement', None)
        if announcement:
            announcement.title = request.POST.get('title')
            announcement.content = request.POST.get('content')
            announcement.save()
            return HttpResponseRedirect(reverse('announcements_list'))
        else:
            raise Http404
        
    else:
        p_id = request.GET.get("p_id")
        choice = request.GET.get('choice')
        print choice
        template_name = "announcements/change_announcement.html"
        announcement = Announcement.objects.get(id=p_id)
        if choice == "change":
            print 'dddd'
            request.session['announcement'] = announcement
            
            content = announcement.content
            title = announcement.title
            print content
        elif choice == 'del':      
            announcement.delete()
            return HttpResponseRedirect(reverse('announcements_list'))
    ctx = {
        'content':content,
        'title':title
    }
#            
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@admin_required
def file_change(request, **kwargs):
    """
    资料删除和修改
    """
    choice = request.GET.get("choice", None)
    f_id = request.GET.get("f_id", None)    
    template_name = "management/sys/file_change.html"
    if request.method == "POST":
        change = False
        File = request.session.get("File")
        title = request.POST.get("title")
        url = request.POST.get("url")
        detail = request.POST.get("detail")
        if title and title != File.title:
            change = True
            File.title = title
        if url and File.url != url:
            print url, 'test'
            change = True
            File.url = url
        if detail and File.detail != detail:
            change = True
            File.detail = detail
    
        if change:
            File.save()
        return HttpResponseRedirect(reverse("management_file_list"))
    else:
        File = get_object_or_404(file_upload, pk=f_id)
        if choice == "change":
            
            request.session['File'] = File
            
            ctx = {
                'File':File
            }
            return render_to_response(template_name, RequestContext(request, ctx))
        else:
            File.delete()
            return HttpResponseRedirect(reverse("management_file_list"))
            
@login_required
@admin_required
def message_del(request, **kwargs):
    """
    留言版删除
    """
    m_id = request.GET.get("message")
    Message = get_object_or_404(message, pk=m_id)
    Message.delete()
    return HttpResponseRedirect(reverse("admin_messages"))


@login_required
@admin_required
def search_fuc(request, **kwargs):
    """
    万能搜索
    """
    data = ""
    template_name = "management/search.html"
    choice = request.GET.get("to_search", None)
    UserBasic = ""
    search_result = []
    L = []
    info_dict = {
    'name':'姓名',
    'number':'编号',
    'role':'用户角色',
    'id_card_number':'身份证号',
    'phone':'电话',
    'mobile':'手机',
    'gender':'性别',
    'start_date':'注册日期',
    'QQ':'QQ',
    'is_void':'空点',
    'is_stock_XR':'股票除权',
    'is_blocked':'冻结',
    'bank_name':'开户银行',
    'bank_account_id':'银行帐号',
    'bank_account_name':'开户姓名',
    'cash':'现金账户余额',
    'store_order':'报单账户余额',
    'store_cash':'订货账户余额',
    'stock_repeat':'股票重复消费余额',
    'stock_rebuy':'股票回购余额',
    'stock_hold':'股票持有总额',
    'mall_single_score':'商城个人积分',
    'mall_team_score':"商城团队积分",
    'store_total_money_A':'A区累计业绩',
    'store_total_money_B':'B区累计业绩',
    'sum_declare':'A网业绩累积值',
    'sum_bonus_recost':'A网回购奖累积值',
    'stock_hold_0devide':'零次拆股股数',
    'stock_hold_1devide':'一次拆股股数',
    'stock_hold_2devide':'两次拆股数',
    'can_devide':'可被拆股次数',
    'stock_hold_max':'股票享受拆股封顶值',
    'proxy_area':'区代',
    'proxy_city':'市代',
    'proxy_province':"省代",
    'can_share_out':'是否能享受分红',
    'adding_ID':'添加者',
    'recommending_id':'推荐人',
    'contacting_ID':'接点人',
    'contact_area':'所在区域',
    'is_central':'是否是中心店',
    'user_central_id':'中心店编号',
    'money':'金额',
    'low_percentage':'小区',
    'day_max':'日封顶',
    'init_money':'启动资金'
    }
    
    if choice == 'search':
        sql = ""
        UserBasic = user_basic.objects.defer('number').all()
        print request.GET
        cursor = connection.cursor()
        content = request.GET.get("content", None)
        print content
        user_number = request.GET.get("number", None)
        L = ['编号', '姓名', '推荐人', '接点人', '添加者', '中心店编号', '空点', '股票除权', '冻结', '是否是中心店', '是否享受分红']
        if content:
            sql = "select number,name,recommending_id,contacting_ID,adding_ID,user_central_id,is_void,is_stock_XR,is_blocked,is_central,can_share_out,%s from V_SUPER_USER_INFO" % (content)
        else:
            sql = "select number,name,recommending_id,contacting_ID,adding_ID,user_central_id,is_void,is_stock_XR,is_blocked,is_central,can_share_out from V_SUPER_USER_INFO" 
        if user_number:
            sql += " where number= '%s'" % user_number
        print sql
        try:
            cursor.execute(sql)  
        except:
            print 'sss'
        result = cursor.fetchall()
        for r in result:
            _result = []
            for i in range(0, len(r)):
                a = r[i]
                if i == 2:
                    try:
                        a = UserBasic.get(id=a).number
#                        a = UserRecommender
                    except:
                        a = "无"
                if i == 3:
                    try:
                        a = UserBasic.get(id=a).number
                    except:
                        a = "无"
                if i == 4:
                    try:
                        a = UserBasic.get(id=a).number
#                        r[i] = Adding.number
                    except:
                        a = "管理员"
                if i == 5:
                    try:
                        a = UserBasic.get(id=a).number
#                        r[5] = UserBasic.number
                    except:
                        a = "无"
                if i == 6 or i == 7 or i == 8 or i == 9 or i == 10:
                    if a == 0:
                        a = "否"
                    else:   
                        a = "是"
                if a == "M":
                    a = "男"
                elif a == "F":
                    a = "女"
                _result.append(a)
            search_result.append(_result)
        content = content.split(",")

        for p in content:
            try:
                L.append(info_dict[p])
            except:
                break
#        print search_result
        file_name = str(datetime.datetime.now())
        print file_name
        UserBasic = PaginatorFuc(request, search_result)
        request.session['Content'] = L
        request.session['Result'] = search_result
        request.session['file_name'] = file_name
#        print search_result
#        try:
#        L = content.split(",")
        print L
#        except:
#            L=""
    ctx = {
        "data":data,
        "L":L,
        'UserBasic':UserBasic,
        "search_result":search_result,
        'info_dict':info_dict
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))


@login_required
@admin_required
def reset_password(request, **kwargs):
    """
    重置用户密码
    """
    from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
    u_id = request.GET.get("u_id", None)
    print u_id
    try:
        UserBasic = user_basic.objects.defer("password_1nd", "user", 'password_2nd').get(id=u_id)
        print UserBasic
        ValueSetting = value_setting.objects.defer('password_1nd', 'password_2nd').all()[0]
        UserBasic.user.set_password(ValueSetting.password_1nd)
        UserBasic.password_1nd = UserBasic.user.password
        UserBasic.password_2nd = make_password(ValueSetting.password_2nd)
        UserBasic.user.save()
        UserBasic.save()
        data = '1'
    except:
        data = '0'
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
@login_required
@admin_required
def extracting_rate(request, **kwargs):
    """
    拨出率统计
    """
    import types
    bonus_style = request.GET.get("bonus_style")

    call_proc = CallProc()

    if not bonus_style:
        proc_name = "get_extracting_rate_20130428"
        call_proc.CallProcFuc_0(proc_name)
        cursor = connection.cursor()
    
        Content = ['A网业绩', 'A网总奖金', 'A网拨出率', '开始日期', '结束日期', '结算发放日期']
        cursor.execute('select * from t_extracting_rate_A_new order by pay_day desc')    
    else:
        proc_name = "get_extracting_rate"
        call_proc.CallProcFuc_0(proc_name)
        cursor = connection.cursor()
        Content = ['C网业绩', 'C网总奖金', 'C网拨出率', '日期']
        cursor.execute('select * from t_extracting_rate_C ORDER BY month DESC')    
    ExtractingRate = cursor.fetchall()
    ExtractingRate = list(ExtractingRate)
    _ExtractingRate = []
    for e in ExtractingRate:
        e = list(e)
        for eData in e:
            if(type(eData) is datetime.date):
                eData = eData.strftime("%Y.%m.%d")
	_ExtractingRate.append(e)
    ExtractingRate = PaginatorFuc(request, ExtractingRate)
    template_name = "management/member/extracting_rate.html"
    request.session['Content'] = Content
    request.session['Result'] = _ExtractingRate
    request.session['file_name'] = "%s拨出率统计" % (str(datetime.datetime.now()))
    ctx = {
        'ExtractingRate':ExtractingRate,
        'bonus_style':bonus_style
    }        
    return render_to_response(template_name, RequestContext(request, ctx))
@login_required
@admin_required 
def management_login_mem(request, **kwargs):
    """
    管理员登录会员的界面
    """
    from django.contrib.auth import authenticate, login, logout
    user_id = request.GET.get("user_number")
    UserBasic = user_basic.objects.get(id=user_id)

#    request.session['password_2nd'] 
    UserBasic.user.backend = 'django.contrib.auth.backends.ModelBackend'

    login(request, UserBasic.user)
    request.session['role'] = UserBasic.role
    request.session['password_2nd'] = True
    
    return HttpResponseRedirect(reverse("member"))
    
