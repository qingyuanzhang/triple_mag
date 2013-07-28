#coding=utf-8
from django.db.models import Q,F
from django.shortcuts import render_to_response,HttpResponseRedirect,RequestContext,render
from TripleMag.apps.decorators import store_required,mem_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
import json 
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from django.contrib.auth.models import User
from TripleMag.apps.decorators import get_user_basic
from TripleMag.apps.money.forms import WithdrawForm,CashTransForm
from TripleMag.apps.money.models import cash_withdraw,cash_trans
from TripleMag.apps.member.models import user_basic,user_contactor
from TripleMag.apps.money.models import bonus_declare_record,bonus_mall_record
from TripleMag.apps.views import PaginatorFuc
from TripleMag.apps.management.models import value_setting
from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
    
@login_required
@mem_required
def index(request, **kwargs):
    """
    电子银行首页
    """
    template_name = "money/base.html"
    return render(request,template_name)
@login_required
def add_member(request):
    return HttpResponseRedirect("/");
    
@get_user_basic
def accounts(request,template_name=None, **kwargs):
    
    template_name = "money/accounts.html"
    UserBasic = kwargs.pop("UserBasic")
    
    ctx = {
        "UserBasic": UserBasic 
    }    
    return render_to_response (template_name,RequestContext(request,ctx))     
    
@login_required
@mem_required
def withdraw(request, **kwargs):
    """
    用户提现申请
    """
    UserBasic = kwargs.pop("Mem")
    template_name = "money/base.html"
    include_template = "money/withdraw.html"
    error = ""
    UserBasic.stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
    UserBasic.sum = UserBasic.cash + UserBasic.stock_rebuy + UserBasic.stock_repeat
    if request.method == "POST":
        CashWithDraw = cash_withdraw(user = UserBasic)
        
        form = WithdrawForm(request.POST,user = request.user,instance = CashWithDraw)
        if form.is_valid():
            withdraw_money = form.cleaned_data['amount']
#            form = WithdrawForm(request.POST,)
           
            if withdraw_money % 100 == 0 and withdraw_money >=200:
                if UserBasic.cash <withdraw_money:
                    error= "你的余额不足"
                else:
                    UserBasic.cash = UserBasic.cash - withdraw_money
                    extra_context = UserBasic.number+"申请提现"+ str( withdraw_money)+"元"
        #            user = User.objects.filter(username = UserBasic.user.username)
                    user = User.objects.get(id = 1)
                    notification.send(user, "withdraw_appl_notice",extra_context,True, request.user)
                    UserBasic.save()
                    form.save()
            else:
                error = "您提取的金额最小为200，而且必须是整百"
    else:
        form = WithdrawForm()
    ctx = {
        "form": form,
        "UserBasic": UserBasic,
        "include_template": include_template,
        "error":error
    }
    return render_to_response (template_name, RequestContext(request,ctx))

@login_required
def trans(request, **kwargs):
    """
    用户转帐
    """
    user = request.user
    UserBasic = user_basic.objects.filter(user = user)[0]
    UserBasic.stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
    UserBasic.sum = UserBasic.cash + UserBasic.stock_rebuy + UserBasic.stock_repeat
    template_name = "money/base.html"
    include_template = "money/transfer.html"
    error = ""
    if request.method == "POST":
        form = CashTransForm(request.POST,user = request.user)
        if form.is_valid():
            UserTo = user_basic.objects.filter(number = form.cleaned_data['user_to'])[0]
            CashTrans = cash_trans(user_from = UserBasic, user_to = UserTo)
            CashTrans.amount = form.cleaned_data['amount']
            if UserTo.id == UserBasic.id:
                error = "不能给自己转帐"
            elif UserTo.role !="MemMax":
                error = "对方不是报单中心"
            else:
                UserBasic.cash = UserBasic.cash - form.cleaned_data['amount']
                UserTo.store_order = UserTo.store_order + form.cleaned_data['amount']
                UserBasic.save()
                UserTo.save()
                CashTrans.save()
                extra_context = UserBasic.number+"给你转入了"+str(form.cleaned_data['amount'])+"元"
                ##这里需要增加提醒 ##
                notification.send(UserTo.user, "tranfs_notice",extra_context,True, request.user)
#                    return HttpResponseRedirect(rev)

    else:   
        form = CashTransForm
        
    ctx = {
        "form": form,
        'UserBasic':UserBasic,
        'include_template':include_template,
	'error':error
    }
    return render_to_response(template_name, RequestContext(request, ctx))

    
@login_required
def withdraw_record(request, **kwargs):
    """
    查看提现记录
    """
    user = request.user
    UserBasic = ""
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    out_put_name = "提现记录导出"
    ValueSetting = value_setting.objects.defer("withdraw_rate").get(id = 1)
    if user.is_superuser or user.first_name == "finance":
        template_name = "management/member/withdraw_record.html"
        include_template = "money/withdraw_record.html"
        if start_time:
            if not end_time:
                CashWithdrawRecord = cash_withdraw.objects.filter(
                                time_start__gte=start_time,state="sure").order_by("-id")
            else:
                CashWithdrawRecord=cash_withdraw.objects.filter(
                        time_start__range =(start_time,end_time),state="sure").order_by("-id")
        else:
            CashWithdrawRecord = cash_withdraw.objects.filter(state="sure").order_by("-id")
        Content = ['编号','昵称','开户银行','开户姓名','银行帐号','提现金额','纳税','实发金额','提现请求时间']
        Result = []
        for R in CashWithdrawRecord:
            R.withdraw_money = R.amount*ValueSetting.withdraw_rate
            R.withdraw_real_money = R.amount - R.withdraw_money 
            result = []
            result.append(R.user.number)
            result.append(R.user.name)
            result.append(R.user.bank_name)
            result.append(R.user.bank_account_name)
            result.append(R.user.bank_account_id)
            result.append(R.amount)
             
            result.append(R.withdraw_money)
            result.append(R.withdraw_real_money)
            try:
                result.append(str(R.time_start.strftime("%Y.%m.%d")))
            except:
                result.append("--")
            Result.append(result)
        request.session['Content'] = Content
        request.session['Result'] = Result
        request.session['file_name'] = "提现记录表"
    else:
        template_name = "money/base.html"
        include_template = "money/withdraw_record.html"
        UserBasic = user_basic.objects.filter(user = user)[0]
        UserBasic.stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        UserBasic.sum = UserBasic.cash + UserBasic.stock_rebuy + UserBasic.stock_repeat
        CashWithdrawRecord = cash_withdraw.objects.filter(user = UserBasic,state="sure" ).order_by("-id")
        for R in CashWithdrawRecord:
            R.withdraw_money = R.amount*ValueSetting.withdraw_rate
            R.withdraw_real_money = R.amount - R.withdraw_money         
        
    CashWithdrawRecord = PaginatorFuc(request,CashWithdrawRecord)

    ctx={
        'CashWithdrawRecord':CashWithdrawRecord,
        'include_template':include_template,
        'UserBasic':UserBasic,
        "out_put_name":out_put_name,
        "start_time":start_time,
        "end_time":end_time
    }
    return render_to_response(template_name,RequestContext(request,ctx))
@login_required
def trans_records(request, **kwargs):
    """
    所有的转入和转出记录
    """
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    user = request.user
    CashTransRecords = ""
    CashTransInRecords = ""
    CashTransOutRecords = ""
    out_put_name = ""
    UserBasic = ""
    if user.is_superuser or user.first_name == "finance":
        if start_time:
            if not end_time:
                CashTransRecords = cash_trans.objects.filter(time__gte=start_time).order_by("-time")
            else:
                CashTransRecords = cash_trans.objects.filter(time__range=(start_time,end_time)).order_by("-time")
        else:
            CashTransRecords = cash_trans.objects.all().order_by("-time")
        template_name = "management/member/trans_records.html"
        Content = ['转出金额','到账时间','转出人编号','转出人姓名','转到人编号','转到人姓名']
        out_put_name = "转帐记录导出"
        Result = []
        for R in CashTransRecords:
            result = []
            result.append(R.amount)
            result.append(str(R.time.strftime("%Y.%m.%d")))
            result.append(R.user_from.number)
            result.append(R.user_from.name)
            result.append(R.user_to.number)
            result.append(R.user_to.name)
            Result.append(result)
        request.session['Content'] = Content
        request.session['Result'] = Result
        request.session['file_name'] = "转帐记录表"
        CashTransRecords = PaginatorFuc(request,CashTransRecords)
    else:
        UserBasic = user_basic.objects.filter(user = user)[0]
        UserBasic.stock_hold = UserBasic.stock_hold_0devide + UserBasic.stock_hold_1devide + UserBasic.stock_hold_2devide
        UserBasic.sum = UserBasic.cash + UserBasic.stock_rebuy + UserBasic.stock_repeat
        CashTransInRecords = cash_trans.objects.filter(user_to = UserBasic)
        CashTransOutRecords = cash_trans.objects.filter(user_from = UserBasic)
        template_name = "money/base.html"
    include_template = "money/trans_records.html"
    ctx = {
        "cash_trans_in_records": CashTransInRecords,
        "cash_trans_out_records": CashTransOutRecords,
        'cash_trans_records':CashTransRecords,
        'include_template':include_template,
        'UserBasic': UserBasic,
        "out_put_name":out_put_name,
        "start_time":start_time,
        "end_time":end_time
    }
    
    return render_to_response(template_name, RequestContext(request,ctx))
    
@login_required
@get_user_basic
def bonus_records(request, **kwargs):
    """
    查看所有的奖金记录
    """    
    #根据用户的角色来查看奖金待作
#    bouns_list = {
#        "admin": model.objects.all(),
#        "store": models.objects.filter(user = UserBasic)
#    }

#    template_name = "money/a_bonus_records.html"
    kwargs.pop('template_name')
    UserBasic = kwargs.pop("UserBasic")
    bonus = bonus_declare_record.objects.filter(user = UserBasic)
    ctx = {
        'bonus': bonus,
        'UserBasic':UserBasic
    }
    return render_to_response(template_name , RequestContext(request,ctx))
    
@login_required
@get_user_basic
def c_bonus_records(request, **kwargs):
    """
    查看C网奖金记录
    """
    template_name = "money/c_bonus_records.html"
    UserBasic = kwargs.pop("UserBasic")
    bonus = bonus_mall_record.objects.filter(user = UserBasic)
    ctx = {
        'bonus': bonus
    }
    return render_to_response(template_name, RequestContext(request,ctx))
    
    
    
    
