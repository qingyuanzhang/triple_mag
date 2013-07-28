#coding=utf-8
from django.db.models import Q,F
from django.shortcuts import render_to_response,HttpResponseRedirect,RequestContext,HttpResponse,render
from TripleMag.apps.decorators import store_required,mem_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json 
import sys,threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from TripleMag.apps.decorators import get_user_basic,mem_required,stock_locked
from TripleMag.apps.stock.forms import StockForm
from TripleMag.apps.stock.models import trade_record,selling_poll,income_record as t_income_record,trend_record
from TripleMag.apps.views import CallProc,PaginatorFuc,stock_line_chart
from TripleMag.apps.member.models import user_basic,user_recommender
from TripleMag.apps.management.models import value_setting

from django.db import connection
import warnings
from warnings import filterwarnings
import MySQLdb as Database
filterwarnings('ignore', category = Database.Warning)
from decimal import *
from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
@login_required
@mem_required
@stock_locked
def index(request, **kwargs):
    """
    股票首页
    """
    template_name = "stock/base.html"
    role = request.session.get('role')
    message = request.GET.get("message",None)
    Mem = kwargs.pop("Mem")
    Mem.stock_hold = Mem.stock_hold_0devide + Mem.stock_hold_1devide + Mem.stock_hold_2devide
    Mem.sum = Mem.cash+Mem.stock_repeat+Mem.stock_rebuy
    ValueSetting = value_setting.objects.all()[0]
    AllSellingPoll = selling_poll.objects.all().order_by("value")
    DirectBuyPoll = AllSellingPoll.filter(user_to = Mem)
    DirectSellingPoll = AllSellingPoll.filter(user_from = Mem,user_to__isnull = False)
    SellingPoll = AllSellingPoll.filter(user_to__isnull = True).order_by("value")
    ValueSetting.stock_value_min_price = ValueSetting.stock_value_now-ValueSetting.stock_value_delta
    ValueSetting.stock_value_max_price =  ValueSetting.stock_value_now+ValueSetting.stock_value_delta
    call_proc = CallProc()
    cursor = connection.cursor()
    cursor.callproc("get_stock_statistics",('','','','',))
    cursor.execute('select @_get_stock_statistics_0')
    overall_total_count = cursor.fetchone()[0]
    
    ChartData = stock_line_chart()
    #计算股票的最大值
#    max_sell = Mem.stock_hold / 1000
#    if max_sell < ValueSetting.sell_max_amount:
#        ValueSetting.sell_max_amount = max_sell
    sell_form = StockForm()
    buy_form = StockForm()
    print Mem,'mmmm'
    ctx = {
        "UserBasic":Mem,
        "sell_form": sell_form,
        'buy_form':buy_form,
        "selling_poll": SellingPoll,
        "direct_selling_poll": DirectSellingPoll,
        "direct_buy_poll":DirectBuyPoll,
        "ValueSetting": ValueSetting,
        "choose":"我的股票",
        'ChartData':ChartData,
        'overall_total_count':overall_total_count
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))

@login_required
@mem_required
@stock_locked
def buy_stock(request,**kwargs):
    """
    购买股票
    """
    
    extra_context = kwargs.pop("error_detail")
    if not extra_context:
        lock = threading.Lock()
        UserBasic = kwargs.pop('Mem')
        buy_amount = 0
        if request.method == "POST": 
            form = StockForm(request.POST,user = request.user)
            if form.is_valid():
                seller_number = form.cleaned_data['n_seller']
                amount = form.cleaned_data['amount']
                _value = Decimal(form.cleaned_data['value'])
                total_money = UserBasic.cash + UserBasic.stock_repeat + UserBasic.stock_rebuy
                
                if total_money< (amount * _value):
                    extra_context = "没有足够的余额"
                else:
                    if not seller_number:
                        Stocks = selling_poll.objects.filter(value__lte = _value).exclude(user_from = UserBasic).order_by('value')

                    else:
                        seller = user_basic.objects.filter(number = seller_number)[0]
                        Stocks = selling_poll.objects.filter(value__lte = _value, user_from = seller).order_by('value')
                    lock.acquire()
        #            try:
                    
                    buy_amount = buy(request,Stocks,amount,UserBasic.id)
                    if buy_amount == 0:
                        extra_context = "购买失败,没有符合你要求的股票"
                    else:
                        extra_context = "你成功买入了"+str(buy_amount)+"股"
        #            finally:
                    lock.release()    
            else:
                extra_context = "二级密码错误"
    return HttpResponse(json.dumps(extra_context),mimetype="application/json")

def buy(request,Stocks, amount, buy_id):
    """
    股票购买不定向
    """
    
    buy_amount=0
    for stock in Stocks:
        if stock.amount >= amount:
            call_proc = CallProc()
            call_proc.CallProcFuc_3('stock_buy',int(buy_id),stock.id,int(amount))
            """
            股票卖出提醒
            """
            buy_amount += amount
            extra_context = "你的股票成功卖出"+str(amount)+"股"
            notification.send(stock.user_from.user, "stock_sold_notice",extra_context,True, request.user)
            break
        else:
            buy_amount += amount
            call_proc = CallProc()
            call_proc.CallProcFuc_3('stock_buy',int(buy_id),stock.id,stock.amount)
            amount = amount - stock.amount
            extra_context = "你的股票成功卖出"+str(stock.amount)+"股"
            notification.send(stock.user_from.user, "stock_sold_notice",extra_context,True, request.user)
    return buy_amount

@login_required
@mem_required
@stock_locked
def direct_stock_buy(request, **kwargs):
    """
    股票定向购买
    """
    error_detail = kwargs.pop("error_detail")
    if not error_detail:
        UserBasic = kwargs.pop("Mem")
        try:
            SellingPollId = int(request.GET.get("sp_id"))
            SellingPoll = selling_poll.objects.get(id = SellingPollId)
            amount = int(request.GET.get("amount"))

            
        except:
            raise Http404
        total_money = UserBasic.cash + UserBasic.stock_repeat +UserBasic.stock_rebuy
        print total_money,amount*SellingPoll.value
        if total_money<(amount*SellingPoll.value):
            request.session['message'] = "您没有足够的余额"
            return HttpResponseRedirect(reverse("stock_index"))
        buy_id = UserBasic.id
        call_proc = CallProc()
        call_proc.CallProcFuc_3('stock_buy',buy_id,SellingPollId,amount)
    else:
        request.session['message'] = error_detail
    return HttpResponseRedirect(reverse("stock_index"))
    
@login_required
@mem_required   
@stock_locked
def sell_stock(request, **kwargs):
    """
    卖出股票
    """
    from decimal import *
    import datetime 
    UserBasic = kwargs.pop("Mem")
    extra_context = kwargs.pop("error_detail")
    print extra_context,'bbbbb'
    if not extra_context:
        template_name = "stock/sell_stock.html"
        amount = 0
        if request.method =="POST":
            today = datetime.datetime.now()
            cursor = connection.cursor()
            prevDate = today + datetime.timedelta(days=1)
            sql_str = "SELECT * FROM rtyk_triple.stock_selling_poll where time >='%s' and time<'%s' and user_from_id=%s"%(today.strftime('%Y-%m-%d'),prevDate.strftime('%Y-%m-%d'),UserBasic.id)
            cursor.execute(sql_str)
            HasSellingStock = cursor.fetchall()
            SellingPoll = selling_poll(user_from = UserBasic)
            form = StockForm(request.POST,user=request.user, instance = SellingPoll)
            if form.is_valid():
                seller_id = UserBasic.id
                user_to = form.cleaned_data['n_seller'].strip().upper()
                value = Decimal(form.cleaned_data['value'])
    #            value = Decimal(stock_value)
                amount = form.cleaned_data['amount']
                if not HasSellingStock:
                    if not user_to and amount>2000:
                        extra_context = "每次出售股票不能大于2000股"
                        return HttpResponse(json.dumps(extra_context),mimetype="application/json")
                    else:
                        if not user_to:
                            to_user_id = None
                        else:   
                            if user_to == UserBasic.number:
                                extra_context = "你不能向自己出售股票"
                                return HttpResponse(json.dumps(extra_context),mimetype="application/json")
                            amount = int(request.POST.get("direct_sell_amount"))
                            
                            to_user = user_basic.objects.filter(number = user_to)[0]
                            extra_context = UserBasic.number+"向你定向售出"+str(amount)+"股,"+"单价"+str(value)+"元,"+"总价"+str(amount*value)+"元."
    #                        notification.send(to_user.user, "stock_sold_notice",extra_context,True, request.user)
                            to_user_id = to_user.id
                            
                        if amount<=(UserBasic.stock_hold_0devide+UserBasic.stock_hold_1devide+UserBasic.stock_hold_2devide):
                            extra_context = "你成功售出"+str(amount)+"股,单价"+str(value)+"元,总价"+str(amount*value)+"元."
        #                    url = reverse("stock_index")+"?message="+extra_context
                            call_proc = CallProc()
                            call_proc.CallProcFuc_4("stock_sell",seller_id,value,amount,to_user_id)
                        else:
                            extra_context = "你的股票余额不足"
                        result = "结算成功"
                        result = "结算失败"
                else:
                    extra_context = "每天只能出售一次股票"
            else:
                extra_context = form.errors.items()[0][1]

    return HttpResponse(json.dumps(extra_context),mimetype="application/json")
#    ctx = {
#        "UserBasic": UserBasic,
#        "sell_form": form ,
#    }
#    return render_to_response(template_name , RequestContext(request,ctx))
            
def get_selling_poll(request, **kwargs):
    """
    ajax刷新股票池
    """
    DirectSellingPoll = ""
    DirectBuyPoll = ""
    if not request.user.is_superuser:
        
        UserBasic = user_basic.objects.get(user = request.user)
        
        SellingPoll = selling_poll.objects.all().order_by("value")
        AllSellingPoll = SellingPoll.filter(user_to__isnull = True).order_by("value")
        
        DirectBuyPoll = SellingPoll.filter(user_to = UserBasic)
        
        DirectSellingPoll = SellingPoll.filter(user_from = UserBasic,user_to__isnull = False)
        print 'sss'
        choose = "我的股票"
    else:
        AllSellingPoll =  selling_poll.objects.all().order_by("value")
        choose = "全部股票"
    template_name = "stock/selling_poll.html"
    ctx = {
        "selling_poll": AllSellingPoll,
        "direct_selling_poll":DirectSellingPoll,
        "direct_buy_poll":DirectBuyPoll,
        "choose": choose
    }

    return render_to_response(template_name ,RequestContext(request ,ctx))
    
@login_required
@get_user_basic
def stock_record(request, **kwargs):
    """
    查看自己的股票售出交易记录
    """
    template_name = kwargs.pop("template_name")
    include_template = "includes/stock_record.html"
    
    if request.user.is_superuser or request.user.first_name == "finance":
        UserBasic = kwargs.pop("UserBasic")
        if not UserBasic:
            SellingRecord = trade_record.objects.all().order_by("-time")
        else:
            SellingRecord = trade_record.objects.filter(seller = UserBasic).order_by("-time")
    else:
        UserBasic = user_basic.objects.filter(user = request.user)
        SellingRecord = trade_record.objects.filter(seller = UserBasic).order_by("-time")
        print SellingRecord
    for sr in SellingRecord:
        sr.sum_price = sr.amount * sr.value
    csv_trade_record(request,SellingRecord)
    SellingRecord = PaginatorFuc(request,SellingRecord)
    
    ctx = {
        "selling_record": SellingRecord,
        "include_template":include_template
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))


@login_required
def income_record(request, **kwargs):
    """
    股票来源记录
    """
    user = request.user
    if not user.is_superuser and user.first_name != "finance":
        UserBasic = user_basic.objects.defer(None).filter(user = user)
        for UBasic in UserBasic:
            IncomeReocrd = t_income_record.objects.filter(to_user = UBasic).order_by("-time")
    else:
        IncomeReocrd = t_income_record.objects.all().order_by("-time")
    csv_income(request,IncomeReocrd)
    template_name = kwargs.pop("template_name")
    include_template = "includes/income_record.html"

    
    IncomeReocrd = PaginatorFuc(request,IncomeReocrd)
    
    ctx={
        'income_record': IncomeReocrd,
        'include_template': include_template
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))




@login_required
def stock_bonus(request, **kwargs):
    """
    股票奖金查看
    """
    user = request.user
    UserBasic = user_basic.objects.defer(None).all()
    cursor = connection.cursor()
    if user.is_superuser or user.first_name =="finance":
        cursor.execute("select * from V_STOCK_RECOMMENDER_BONUS")
    else:
        UserToId = UserBasic.filter(user = user)[0].id
        cursor.execute("select * from V_STOCK_RECOMMENDER_BONUS where usr_to = %s",UserToId)
    template_name = kwargs.pop("template_name")
    Stock_Bonus = []


    result = cursor.fetchall()
    for r in result:
        print r
        UserTo = UserBasic.get(id = r[0])
        URecommender = UserBasic.get(id = r[3])
        _StockBonus = []
        _StockBonus.append(UserTo.number)
        _StockBonus.append(UserTo.name)
        _StockBonus.append(URecommender.number)
        _StockBonus.append(URecommender.name)
        _StockBonus.append(r[1])
        _StockBonus.append(r[2])
        Stock_Bonus.append(_StockBonus)
    csv_stock_bonus(request,Stock_Bonus)
    StockBonus = PaginatorFuc(request,Stock_Bonus)
    cursor.close()
    connection.close()
#    for UBasic in UserBasic:
#        try:
#            UserRecommender = user_recommender.objects.defer('recommended').filter(recommending = UBasic)
#            for URecommender in UserRecommender:
#                StockBonus = trade_record.objects.defer("time","ex_return",'buyer').filter(buyer = URecommender)
#                if StockBonus:
#                    for s in StockBonus:
#                        
#                        s.recommender_name = URecommender.recommending.name
#                        s.recommender_number = URecommender.recommending.number
#                    Stock_Bonus.append(StockBonus)
#        except:
#            print '没有下级'
#    Stock_Bonus = PaginatorFuc(request, Stock_Bonus)
#    for s in Stock_Bonus:
#        for d in s:
#            print d
    ctx = {
        "stock_bonus":StockBonus,
        'include_template': 'includes/stock_bonus.html'
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
    
    
    
    
    
    
    
@login_required
@mem_required
@stock_locked
def cancle_stock(request, **kwargs):
    """
    清除股票记录
    """
    UserBasic = user_basic.objects.filter(user = request.user)[0]
    SellingPollId = request.GET.get("sp_id")
    print SellingPollId
    SellingPoll = selling_poll.objects.get(user_from = UserBasic,id=SellingPollId)
    
    if not SellingPoll:
        raise Http404
    else:
        call_proc = CallProc()
        call_proc.CallProcFuc_1('stock_return',SellingPollId)
    return HttpResponseRedirect(reverse("stock_index"))
    
    
    
    
def csv_income(request,IncomeReocrd):
    """
    股票来源csv
    """
    from datetime import *
    Content=['用户编号',"用户姓名","来源类型","数量","来源时间"]
    Result = []
    for R in IncomeReocrd:
        result = []
        result.append(R.to_user.number)
        result.append(R.to_user.name)
        result.append(R.get_type_display())
        result.append(R.amount)
        result.append(str(R.time.strftime("%Y.%m.%d")))
        Result.append(result)
    file_name = "股票来源记录%s"%(datetime.now())
    request.session['file_name'] = file_name
    request.session['Content'] = Content
    request.session['Result'] = Result
def csv_stock_bonus(request,StockBonus):
    """
    股票奖金记录导出
    """
    from datetime import *
    Content =['推荐人编号','推荐人姓名','直荐人编号','直荐人姓名','获得奖金','获得时间']
    Result = StockBonus
    file_name = "股票奖金记录%s"%(datetime.now())
    request.session['file_name'] = file_name
    request.session['Content'] = Content
    request.session['Result'] = Result
def csv_trade_record(request,StockRecord):
    """
    股票售出记录查看
    """
    from datetime import *
    Content=['卖股者编号','卖股者姓名','买股者编号','买股者姓名','交易数量','交易单价','交易总价','成交时间','抽税','回购','返给上级','最后所得']
    Result = []
    for R in StockRecord:
        result = []
        result.append(R.seller.number)
        result.append(R.seller.name)
        result.append(R.buyer.number)
        result.append(R.buyer.name)
        result.append(R.amount)
        result.append(R.value)
        result.append(R.sum_price)
        result.append(R.time.strftime("%Y.%m.%d"))
        result.append(R.tax)
        result.append(R.repo)
        result.append(R.ex_return)
        result.append(R.gain)
        Result.append(result)
    file_name = "股票售出记录%s"%(datetime.now())
    request.session['file_name'] = file_name
    request.session['Content'] = Content
    request.session['Result'] = Result
def del_session(request):
    message = request.session.get("message")
    if message:
        del request.session['message']
        return HttpResponse(json.dumps(message),mimetype="application/json")
    
def load_stock_chart(request,**kwargs):
    """
    加载股票曲线图
    """
    template_name = "includes/stock_chart.html"
    ChartData = stock_line_chart()
    ctx = {
        "ChartData":ChartData
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
    

