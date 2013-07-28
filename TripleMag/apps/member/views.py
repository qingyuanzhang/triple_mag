#coding=utf-8
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json 
from django.core.urlresolvers import reverse

from TripleMag.apps.decorators import get_user_basic
from TripleMag.apps.member.models import *
from TripleMag.apps.member.forms import ChangeInfoApplForm, MessageForm, MemVipApllForm
from TripleMag.apps.management.models import file_upload, member_lv_money, value_setting
from TripleMag.apps.decorators import store_required, mem_required, admin_or_store_required
from TripleMag.apps.money.models import bonus_unpaid, bonus_declare_record, bonus_mall_record, extra_bonus
from TripleMag.apps.views import PaginatorFuc, verify_password_2nd, CallProc, get_submmit_level
from TripleMag.apps.management.views import csv_fuc, csv_fuc_c
from TripleMag.apps.store.forms import AddressForm
from django.db import connection
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
from datetime import *

from notification.models import *
from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@login_required 
@mem_required   
def index(request, **kwargs):
    """
    会员首页
    """
    error = ""
    template_name = "member/base.html"
    UserBasic = kwargs.pop("Mem")
    request.session['contactor_name'] = UserBasic.name
    print request.session['contactor_name']
    ValueSetting = value_setting.objects.defer("grade_summit", 'mall_VIP_threshold').all()[0]
    UserBasic = get_submmit_level(UserBasic=UserBasic)
    
    
#    cursor = connection.cursor()
#    try:
#        cursor.execute('SELECT FA_SUM.father_id as min_id , max(MA_SUM.id) as summit_level FROM (SELECT FATHER.id AS father_id , count(SON.id) AS summit_son_number FROM member_user_recommender AS RECC INNER JOIN member_user_basic AS FATHER ON FATHER.id = RECC.recommending_id INNER JOIN member_user_basic AS SON ON SON.id = RECC.recommended_id ,management_value_setting AS SETTING WHERE SON.mall_team_score > SETTING.grade_summit GROUP BY FATHER.id AS FA_SUM INNER JOIN management_mall_summit AS MA_SUM ON FA_SUM.summit_son_number >= MA_SUM.summit_num where FA_SUM.father_id=%s GROUP BY min_id',UserBasic.id)
#        cursor.execute('SELECT `V_SETTLE_CWEB_BASIC`.`level_name`,`V_SETTLE_CWEB_BASIC`.`threshold_value`,`V_SETTLE_CWEB_BASIC`.`gain_rate`,`V_SETTLE_CWEB_BASIC`.`is_summit` FROM `rtyk_triple`.`V_SETTLE_CWEB_BASIC` where id=%s',UserBasic.id)
#        level = cursor.fetchall()[0]
#        is_summit = level[3]
#        UserBasic.level = level[0]
#        UserBasic.is_summit = is_summit
#    except:
#        UserBasic.level = "新手上路"
#        UserBasic.is_summit = False
    notices = Notice.objects.notices_for(request.user, on_site=True, unseen=True)
    request.session['ValueSetting'] = ValueSetting
    request.session['name'] = UserBasic.name
    if request.method == "POST":
        password_2nd = request.POST.get("password_2nd")
        result = verify_password_2nd(password_2nd, request.user)
        if result:
            request.session['password_2nd'] = True
            return HttpResponseRedirect(reverse("member_index"))
        else:
            error = "二级密码错误"
    ctx = {
        'UserBasic':UserBasic,
        'error':error,
        "notices":notices
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@mem_required
def member_index(request, **kwargs):
    """
    会员信息和电子银行首页
    """
    template_name = "member/member.html"
    
    UserBasic = kwargs.pop("Mem")
    
    ctx = {
        "UserBasic": UserBasic
    }
    return render_to_response(template_name, RequestContext(request, ctx))
@login_required     
@mem_required
@get_user_basic
def member_info(request, **kwargs):
    """
    会员查看自己的信息
    """
    query = request.GET.get("query")
    try:
        query = query.split("_")

    except:
        raise Http404
    template_name = kwargs.pop("template_name", "member/member_info.html")
    ctx = {
        "member_info" :query_result(query, user_number),
    }
    return render_to_response(template_name, RequestContext(request, ctx)) 

@login_required     
@get_user_basic
def member_details(request, template_name=None , **kwargs):
    """
    会员和报单中心查看自己的详细信息
    """
    UserBasic = kwargs.pop("UserBasic")
    request.session['subject'] = "member_center"
    UserAddress = ""
    role = ""
    Level = ""
    UserRecommender = ""
    UMid = ""
    UserContactor = ""
    UMax = ''
    error3 = "" 
    error1 = request.GET.get("error1")
    error2 = request.GET.get("error2")
    ValueSetting = value_setting.objects.defer("stock_share_out_min_amount").get(id=1)
    if not UserBasic:
        try:
            UserBasic = user_basic.objects.filter(user=request.user)[0]
        except:
            raise Http404
    try:
        UserAddress = user_address.objects.filter(user=UserBasic).order_by("id")[0]
    except:
        UserAddress = None
    try:
        UserRecommender = user_recommender.objects.filter(recommended=UserBasic)[0]
        UserBasic.recommending_id = UserRecommender.recommending.number
        UserBasic.recommending_name = UserRecommender.recommending.name
    except:
        UserRecommender = user_recommender(recommended=UserBasic)
        UserBasic.recommending_id = "无"
        UserBasic.recommending_name = "无"
    if UserBasic.role != "MemMin" and UserBasic.role != "MinVIP":
        try:
            UserMidMem = user_mid_mem.objects.filter(user=UserBasic)
            print UserMidMem, "UserMidMem"
            UMid = UserMidMem[0]
            UserBasic.level = UMid .level.level
	    UserBasic.level_name = UMid.level.name
            Level = member_lv_money.objects.all()
        except:
            pass
        try:    
            UserContactor = user_contactor.objects.filter(contacted=UserBasic)[0]
            UserBasic.contacting_id = UserContactor.contacting.number
            UserBasic.contacting_name = UserContactor.contacting.name
            UserBasic.contact_area = UserContactor.contact_area
        except:
            UserContactor = user_contactor(contacted=UserBasic)
            UserBasic.contacting_id = "无"
            UserBasic.contacting_name = "无"
            UserBasic.contact_area = "无"
    
    UserCentralUsual = None
    #报单中心信息
    if UserBasic.role == "MemMax":
        print UserBasic.role, "================"
        try:
            UserMaxMem = user_max_mem.objects.filter(user_mid=UMid)
            print UserMaxMem, "bbbbbbb"
            UMax = UserMaxMem[0]
            print UMax, "==================="
            if not UMax.is_central:
                try:
                    UserCentralUsual = user_central_usual.objects.filter(user_usual=UMax)[0] 
                    print UserCentralUsual, 'ssss'
                    UserBasic.user_central_number = UserCentralUsual.user_central.user_mid.user.number
                    UserBasic.user_central_name = UserCentralUsual.user_central.user_mid.user.name
                except:
                    print 'sss'
            if UMax.is_central == True:
                UserBasic.is_central = True
            else:
                UserBasic.is_central = False
        except:
            print 'ss'
    UserBasic.sum = UserBasic.cash + UserBasic.stock_rebuy + UserBasic.stock_repeat
    try:
        UserAdder = user_adder.objects.defer('adding').filter(added=UserBasic)[0]
    except:
        UserAdder = None
    if request.method == "POST":
        can_share_out = request.POST.get("can_share_out")
        if can_share_out:
            if not UserBasic.can_share_out:
                UserBasic.can_share_out = True
                extra_context = "申请分红成功"
                users = User.objects.filter(is_superuser=True)
                notification.send(UserBasic.user, "share_appl", extra_context, True, request.user)
        else:
            if UserBasic.can_share_out:
                UserBasic.can_share_out = False

        id_card_number = request.POST.get("id_card_number")
        if id_card_number:
            UserBasic.id_card_number = id_card_number
        stock_hold_max = request.POST.get("stock_hold_max")
        if stock_hold_max:
            UserBasic.stock_hold_max = stock_hold_max
        number = request.POST.get("number")
        if number:
            UserBasic.number = request.POST.get("number")
        bank_account_id = request.POST.get("bank_account_id")
        if bank_account_id:
            UserBasic.bank_account_id = bank_account_id
        city = request.POST.get("city")
        if city:
            UserBasic.city = city
        role = request.POST.get("role")
        can_devide = request.POST.get("can_devide")
        if can_devide :
            if not UserBasic.can_devide:
                UserBasic.can_devide = True
        else:
            if UserBasic.can_devide:
                UserBasic.can_devide = False
        is_void = request.POST.get("is_void")
        if is_void :
            if not UserBasic.is_void:
                UserBasic.is_void = True
        else:
            if UserBasic.is_void:
                UserBasic.is_void = False
        if role:
            UserBasic.role = role
            if role == "MemVIP":
                extra_context = "恭喜你成为了商城VIP"
                notification.send(UserBasic.user, "vip_appl", extra_context, True, request.user)
                MinUpgradeRecord = min_upgrade_record.objects.filter(user=UserBasic)
                if MinUpgradeRecord:
                    UserBasic.bank_name = MinUpgradeRecord[0].bank_name
                    UserBasic.bank_account_id = MinUpgradeRecord[0].bank_account_id
                    UserBasic.bank_account_name = MinUpgradeRecord[0].bank_account_name
                    UserBasic.id_card_number = MinUpgradeRecord[0].id_card_number
                    MinUpgradeRecord.state = "sure"
                    MinUpgradeRecord.save()
                    
            elif role == "MemMax":
                UMax = user_max_mem(user_mid=UMid)
                UMax.save()
		                            
            elif role == "MemMin":
                try:
                    UMax.delete()
                except:
                    pass
        user_central = request.POST.get("user_central")
        if user_central:
            _userBasic = user_basic.objects.get(number=user_central)
            print _userBasic, "_userBasic"
            if _userBasic:
                _userMidMem = user_mid_mem.objects.get(user=_userBasic)
                
                print _userMidMem, "_userMidMem"
                if _userMidMem:
                    _userMaxMem = user_max_mem.objects.get(user_mid=_userMidMem)
                    if UserCentralUsual and _userMaxMem:
                        UserCentralUsual.user_central = _userMaxMem
                        UserCentralUsual.save()
                    if not UserCentralUsual and _userMaxMem:
                        print _userMaxMem, "======================"
                        UserCentralUsual = user_central_usual()
                        UserCentralUsual.user_central = _userMaxMem
                        UserCentralUsual.user_usual = UMax
                        UserCentralUsual.save()
                        
        bank_name = request.POST.get("bank_name")
        if bank_name:
            UserBasic.bank_name = bank_name
        phone = request.POST.get("phone")
        if phone:
            UserBasic.phone = phone
        QQ = request.POST.get("QQ")
        if QQ:
            UserBasic.QQ = QQ
            
        name = request.POST.get("name")
        if name:
            UserBasic.name = name
        bank_account_name = request.POST.get("bank_account_name")
        if bank_account_name:
            UserBasic.bank_account_name = bank_account_name
        mobile = request.POST.get("mobile")
        if mobile:
            UserBasic.mobile = mobile
        gender = request.POST.get("gender")
        if gender:
            UserBasic.gender = gender
        start_date = request.POST.get("start_date")
        if start_date:
            UserBasic.start_date = start_date
        
        level = request.POST.get("level")
        if level:
            if UMid.level.id != level:
                _Level = Level.get(id=level)
                upgrade_choice = request.POST.get("upgrade_choice")
                
                #if UserBasic.is_void:
                 #   UMid.init_money = _Level.money - UMid.level.money 
                  #  UserBasic.is_void = False
                   # UserBasic.save()
               # else:
                #    UMid.init_money = _Level.money 

                if upgrade_choice:
                    if UserBasic.is_void:
                        UMid.init_money = _Level.money - UMid.level.money 
                        UserBasic.is_void = False
                        UserBasic.save()
                    else:
                        UMid.init_money = _Level.money 
                    call_proc = CallProc()
                    call_proc.CallProcFuc_2("member_update", UserBasic.id, _Level.money)
                UMid.level = _Level
                UMid.save()
        recommending = request.POST.get("recommending")
        if recommending:
#            try:

            UBasic = user_basic.objects.defer(None).filter(number=recommending)[0]
            
            UserRecommender.recommending = UBasic
            UserRecommender.save()
#            except:
#                error1 = "推荐人不存在"
        proxy_style = request.POST.get("proxy_style")
        if proxy_style:
            if proxy_style == '1':
                UserBasic.proxy_city = None
                UserBasic.proxy_area = None
                UserBasic.proxy_province = None
            else:
                proxy_province = request.POST.get("proxy_province")
                proxy_city = request.POST.get("proxy_city")
                proxy_area = request.POST.get("proxy_area")
                UserBasic.proxy_city = proxy_city
                UserBasic.proxy_area = proxy_area
                UserBasic.proxy_province = proxy_province
        contacting = request.POST.get("contacting")
        if contacting:
            try:
                UBasic = user_basic.objects.defer(None).filter(number=contacting)[0]
                UserContactor.contacting = UBasic
                UserContactor.save()
            except:
                error2 = "接点人不存在"
        contact_area = request.POST.get("contact_area", None)
        if contact_area:
            if UserContactor:
                if UserContactor.contact_area != contact_area:
                    UserContactor.contact_area = contact_area
                    UserContactor.save()
            else:
                UserContactor = user_contactor.objects.filter(contacted=UserBasic)[0]
                    
        style = request.POST.get("style")
        if style:
            if style == '1':
                UMax.is_central = False
            else:
                UMax.is_central = True
            UMax.save()
        try:
            UserBasic.save()
        except:
	    error3 = "编号不能重复"
        url = reverse("management_change_mem_info") + "?user_number=" + UserBasic.number
        if error1:
            url += "&error1=" + error1
        if error2:
            url += "&error2=" + error2
        return HttpResponseRedirect(url)
    UserBasic.stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
#    ValueSetting = request.session.get('ValueSetting')
    try:
        grade_summit = ValueSetting.grade_summit
        mall_VIP_threshold = ValueSetting.mall_VIP_threshold
    except:
        grade_summit = None
        mall_VIP_threshold = None
    UserBasic = get_submmit_level(UserBasic=UserBasic)
#    count_a = 0
#    count_b=0
#    count_sum = 0
#    count_info = request.session.get("count_info")
#    if not count_info:
    count_info = getCountInfo(UserBasic.id)
    #    request.session["count_info"] = count_info
    count_a = count_info[5]
    count_b = count_info[6]
    count_sum = count_info[7]


    ctx = {
        'UserBasic': UserBasic,
        'UserAddress':UserAddress,
        "role": UserBasic.role,
        "Level":Level,
        "grade_summit":grade_summit,
        "mall_VIP_threshold":mall_VIP_threshold,
        "stock_share_out_min_amount":ValueSetting.stock_share_out_min_amount,
        "count_a":count_a,
        "count_b":count_b,
        "count_sum":count_sum,
        "UserAdder":UserAdder,
        "error1":error1,
        "error2":error2,
        "error3":error3
    }
    return render_to_response(template_name, RequestContext(request, ctx)) 
def getCountInfo(user_id):
    """
    获取A、B的业绩和总的业绩
    """
    from TripleMag.apps.views import CallProc
    proc_name = "get_contactor_information"
    call_proc = CallProc()
    cursor = connection.cursor()
    
    call_proc.CallProcFuc_1(proc_name, user_id)
    cursor.execute('select * from t_cont_info where my_id=%s', user_id)
    result = cursor.fetchall()[0]
    return result
@login_required 
@mem_required    
def upgrade_appl_index(request, **kwargs):
    """
    会员升级申请
    """
    UserBasic = kwargs.pop('Mem')
    template_name = "member/upgrade.html"
    error = ""
    Upgrade = member_mid_upgrade_record.objects.filter(user=UserBasic, state="wait")
    if request.method == "POST":
        try:
            Upgrade = member_mid_upgrade_record(user=UserBasic)
            Upgrade.save()
            admin = User.objects.get(id=1)
            extra_context = UserBasic.number + "申请升级报单中心"
            notification.send(admin, "store_appl_notice", extra_context, True, request.user)
            return HttpResponseRedirect(reverse("member_detail"))
        except:
            error = "你的申请请在处理中，请耐心等待"
    ctx = {
        "error":error,
        "has_exit": Upgrade,
        "UserBasic":UserBasic
    }
    return render_to_response(template_name, RequestContext(request, ctx)) 
    

@login_required 
@mem_required
def change_info(request, **kwargs):
    """
    会员修改自己的信息
    """
    UserBasic = kwargs.pop("Mem")
    change_conent = request.GET.get("change_conent")
    try:
        change = change_conent.split("_")
    except:
        return HttpResponse(json.dumps('0'), mimetype="application/json")
    f = change[0]
    c = change[1]
    if f == "mobile":
        UserBasic.mobile = c
    elif f == "phone":
        UserBasic.phone = c
    elif f == "QQ":
        UserBasic.QQ = c
    UserBasic.save()
    return HttpResponse(json.dumps('1'), mimetype="application/json")
    
@login_required 
@mem_required        
def change_info_appl(request, **kwargs):
    """
    会员信息修改申请
    """

    UserBasic = kwargs.pop("Mem")
    template_name = "member/change_info_appl.html"
    if request.method == "POST":
        form = ChangeInfoApplForm(request.POST, user=request.user)
        has_exit = "信息错误"
        print form
        if form.is_valid():
            UserModifyRecord = user_modify_record.objects.filter(user=UserBasic, state="wait")
            if not UserModifyRecord:
                UserModifyRecord = user_modify_record(user=UserBasic, state="wait")
                form = ChangeInfoApplForm(request.POST, user=request.user, instance=UserModifyRecord)
                form.save()
                extra_context = UserBasic.name + "提交了信息修改申请"
                users = User.objects.filter(is_superuser=True)
                notification.send(users, "announcement_notice", extra_context, True, request.user)
                return HttpResponseRedirect(reverse('member_index'))
            else:
                has_exit = "您已经有申请在处理中，请耐心等候"
    else:
        form = ChangeInfoApplForm()
        has_exit = ""
    ctx = {
        'UserBasic':UserBasic,
        'form':form,
        'has_exit': has_exit
    }
    return render_to_response(template_name, RequestContext(request, ctx)) 
    
@login_required 
def file_download(request, **kwargs):
    """
    资料下载
    """
    template_name = kwargs.pop("template_name")
    files = file_upload.objects.all().order_by("-id")
    
    for f in files:
        file_url = f.url.name
        file_url = file_url.split("/")
        f.name = file_url[2]
        
    files = PaginatorFuc(request, files)
    ctx = {
        "files": files
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required 
def download(request, **kwargs):
    """
    下载
    """
    from django.utils.http import urlquote
    
    file_name = request.GET.get("file_name")
    file_path = "/home/rtyk/webapps/static/files/" + file_name
    
    f = open(file_path.encode('utf-8'))
#    data = f.read()
#    f.close()
#    def readFile(fn, buf_size=262144):
#        f = open(fn, "rb")
#        while True:
#            c = f.read(buf_size)
#            if c:
#                yield c
#            else:
#                break
#        f.close()
#    response = HttpResponse(readFile(file_path),mimetype='application/force-download') 
    response = HttpResponse(f.read(), mimetype='application/force-download') 
    
    response['Content-Disposition'] = 'attachment; filename=%s' % urlquote(file_name)

#    response = HttpResponse(mimetype='application/force-download')
#    response['Content-Disposition'] = 'attachment; filename=%s' % urlquote(file_name)
#    d = urlquote(file_path)
#    print d
#    response['X-Sendfile'] = urlquote("/home/hump/TripleMag-env/TripleMag/TripleMag/static/files/")
    return response

@login_required
def messages(request, **kwargs):
    """
    查看留言
    """
    try:
        UserBasic = user_basic.objects.filter(user=request.user)[0]
    except:
        UserBasic = None
    form = ""
    if request.method == "POST":
        if "leave_message" in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                Message = message(user=UserBasic, content=form.cleaned_data['content'])
                Message.save()
                extra_context = UserBasic.number + "给你留言了"
                users = User.objects.filter(is_superuser=True)
                notification.send(users, "announcement_notice", extra_context, True, request.user) 
        elif "to_reply" in request.POST:
            message_id = request.POST.get("message_id")
            reply_content = request.POST.get("reply")
            Message = message.objects.get(id=message_id)
            Message.reply = reply_content
            Message.save()
    else:
        form = MessageForm
    if request.user.is_superuser:
        template_name = "management/sys/messages.html"
        Messages = message.objects.all().order_by("-id")
    else:
        Messages = message.objects.filter(user=UserBasic)
        template_name = "member/messages.html"
        
    
    ctx = {
        'form': form,
        'Messages': Messages,
        'UserBasic':UserBasic
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
        
@login_required
def reply(request, **kwargs):
    """
    回复
    """      
    template_name = "member/reply.html"
    content = request.GET.get("content")
    m_id = request.GET.get("m_id")
    
    Message = message.objects.get(id=m_id)
    Message.reply = content
    Message.save()
    
    ctx = {
        "Message":Message
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def bonus_center(request, **kwargs):
    """
    奖金中心
    """
    try:
        template_name = "member/bonus.html"
        UserBasic = user_basic.objects.defer("id", "role").get(user=request.user)
        ctx = {
            "UserBasic":UserBasic
        }
        return render_to_response(template_name, RequestContext(request, ctx))
    except:
    
        raise Http404


@login_required
def a_bonus(request, **kwargs):
    """
    电子银行
    """
    template_name = "member/every_counter_bonus.html"
    include_template = kwargs.pop("include_template")
    bouns_style = kwargs.pop("bonus_style")
    print bouns_style, include_template, template_name
    try:
        UserBasic = user_basic.objects.defer("id", "role", "number").filter(user=request.user)[0]
    except:
        raise Http404
    BonusRecords = ""
    if UserBasic.role == "MemMin":
        BonusRecords = bonus_mall_record.objects.filter(user=UserBasic).order_by("-time")
    else:
        if bouns_style == "a_bonus":
            UserMidMem = user_mid_mem.objects.filter(user=UserBasic)[0]
            BonusRecords = bonus_declare_record.objects.filter(mid=UserMidMem).order_by("-time")
            print BonusRecords
            csv_fuc(request, BonusRecords)
        elif bouns_style == "c_bonus":
            BonusRecords = bonus_mall_record.objects.filter(user=UserBasic).order_by("-time")
            csv_fuc_c(request, BonusRecords)
    BonusRecords = PaginatorFuc(request, BonusRecords)
    print BonusRecords
    ctx = {
        'BonusRecords': BonusRecords,
        'UserBasic': UserBasic,
        'include_template':include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def unpaid_bonus(request, **kwargs):
    """
    不发放的奖金的查看
    """
    cursor = connection.cursor()

    if request.user.is_superuser or request.user.first_name == "finance":
        UserBasic = user_basic.objects.defer("number", "name", "id").all()
        cursor = connection.cursor()
        
        CBonus = {}
        cursor.execute('select * from V_car_bonus')
        CarBonus = cursor.fetchall()
        for CB in CarBonus:
            print CB
            UBasic = UserBasic.get(id=CB[1])
            UBasic.amount = CB[0]
            CBonus[UBasic.id] = UBasic
#            print 

        HBonus = {}
        cursor.execute('select * from V_house_bonus')
        HouseBonus = cursor.fetchall()
        for HB in HouseBonus:
            UBasic = UserBasic.get(id=HB[1])
            UBasic.amount = HB[0]
            HBonus [UBasic.id] = UBasic
            
        TBonus = {}
        cursor.execute('select * from V_travel_bonus')
        TravelBonus = cursor.fetchall()
        for TB in TravelBonus:
            UBasic = UserBasic.get(id=TB[1])
            UBasic.amount = TB[0]
            TBonus[UBasic.id] = UBasic


        print UserBasic
    else:
    
        
        try:
            UserBasic = user_basic.objects.defer("id").filter(user=request.user)[0]
        except:
            raise Http404
        print UserBasic.id, 'test'
    
        cursor.execute('select * from V_car_bonus where to_user_id = %s', UserBasic.id)
        try:
            CarBonus = cursor.fetchall()[0]
            CBonus = CarBonus[0]
        except:
            CBonus = "无"
#            print 
        cursor.execute('select * from V_house_bonus where to_user_id = %s', UserBasic.id)
        try:
            HouseBonus = cursor.fetchall()[0]
            HBonus = HouseBonus[0]
        except:
            HBonus = "无"

        cursor.execute('select * from V_travel_bonus where to_user_id = %s', UserBasic.id)
        try:
            HouseBonus = cursor.fetchall()[0]
            TBonus = HouseBonus[0]
        except:
            TBonus = "无"
    cursor.execute('select * from V_share_bonus')
    try:
        ShareBonus = cursor.fetchall()[0]
        SB = ShareBonus[0]
    except:
        SB = "无"
    cursor.execute('select * from V_love_bonus')
    try:
        LoveBonus = cursor.fetchall()[0]
        LB = LoveBonus[0]
    except:
        LB = "无"

    template_name = kwargs.pop("template_name")
    include_template = "includes/extra_bonus.html"
    ctx = {
        "HBonus":HBonus,
        "TBonus":TBonus,
        "CBonus":CBonus,
        "SBonus":SB,
        "LBonus":LB,
        "include_template":include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))


def manage_address(request, **kwargs):
    """
    修改地址
    """
    template_name = "member/manage_address.html"
    try:
        UserBasic = user_basic.objects.defer(None).get(user=request.user)
    except:
        raise Http404
    if request.method == "POST":
        UserAddressForm = AddressForm(request.POST)
        print UserAddressForm
        if UserAddressForm.is_valid():
            Address = user_address(user=UserBasic)
            UserAddressForm = AddressForm(request.POST, instance=Address)
            UserAddressForm.save()
            return HttpResponseRedirect(reverse("manage_address"))
    else:
        UserAddressForm = AddressForm()
    UserAddress = user_address.objects.filter(user=UserBasic).order_by("-id")
    UserAddress = PaginatorFuc(request, UserAddress, number=5)
    ctx = {
        "UserAddress":UserAddress,
        "UserAddressForm":UserAddressForm,
        "UserBasic":UserBasic
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
@mem_required
def mem_share_appl(request, **kwargs):
    """
    分红申请
    """
    
    ValueSetting = request.session.get("ValueSetting")
    
    UserBasic = user_basic.objects.get(user=request.user)
    print UserBasic
    if UserBasic:
        stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        print stock_hold
        print ValueSetting.grade_summit
        if stock_hold >= ValueSetting.grade_summit:
            extra_context = UserBasic.number + "申请分红"
            print extra_context
            users = User.objects.filter(is_superuser=True)
            notification.send(users, "share_appl", extra_context, True, request.user)
            return HttpResponseRedirect(reverse("member_details"))
    else:
        raise Http404
    
@login_required
def mem_vip_appl(request, **kwargs):
    """
    VIP申请提醒
    """
    template_name = "member/memmin_upgrade_appl.html"
    MinUpgradeRecord = ""
    has_appl = False
    try:
        UserBasic = user_basic.objects.defer(None).get(user=request.user)
    except:
        raise Http404
    if request.method == "POST":

        bank_name_list = request.POST.get("bank_name_list")
        MinUpgradeRecord = min_upgrade_record(user=UserBasic)
        form = MemVipApllForm(request.POST, user=request.user)
        print form
        if form.is_valid():
            form = MemVipApllForm(request.POST, user=request.user, instance=MinUpgradeRecord)
            form.save()
            extra_context = UserBasic.number + "申请成为VIP"
            print extra_context
            users = User.objects.filter(is_superuser=True)
            notification.send(users, "vip_appl", extra_context, True, request.user)
            return HttpResponseRedirect(reverse("member_details"))
    else:
        MinUpgradeRecord = min_upgrade_record.objects.defer(None).filter(user=UserBasic)
        form = MemVipApllForm()
        if MinUpgradeRecord:
            has_appl = True
    ctx = {
        'form':form,
        'has_appl':has_appl
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@login_required
def mem_conactor(request, **kwargs):
    """
    会员查看自己的三代接点人关系
    """
    UConactor = ""
    template_name = "member/conactor.html"
    UserBasic = ""
    try:
        UBasic = user_basic.objects.defer('name', 'is_void').all()
        UserBasic = UBasic.get(user=request.user)
        UConactor = user_contactor.objects.filter(contacting=UserBasic)

    except:
        raise Http404
    if not UConactor:
        chart_data = ""
    else:
        user_id = UConactor[0].contacted.id
        request.session['contactor_name'] = UserBasic.name
        call_proc = CallProc()
        cursor = connection.cursor()
        
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
                _data += "[{v:\'" + str(r[2]) + "\', f: \'" + str(r[2])

                _data += "</a><br />A区<b class=\"color_em_purple\">" + str(r[5])
                _data += "</b>|B区<b class=\"color_em_purple\">" + str(r[6]) + "</b>"
                _data += "<br />" + str(r[8]) + "级代理'},"
                try:
                    father_number = c[father_id]
                    _data += "\'" + father_number + "\',\'" + str(r[3]) + "区\'],"
                except:
                    _data += "\'\',\'" + str(r[3]) + "区\'],"
                c[my_id] = r[2]
                chart_data += _data
        chart_data = chart_data[:-1]

        chart_data += "]"
    ctx = {
        "chart_data":chart_data,
        "UserBasic":UserBasic
    }
    return render_to_response(template_name, RequestContext(request, ctx))


