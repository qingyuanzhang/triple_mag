#coding=utf-8
from django.db.models import Q,F
from django.shortcuts import render_to_response,HttpResponseRedirect,RequestContext,HttpResponse,render
from TripleMag.apps.decorators import store_required,mem_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import RequestContext

from decimal import *
import json 
import sys,threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from TripleMag.apps.decorators import get_user_basic,store_required,admin_or_store_required,can_store_declare
from TripleMag.apps.store.forms import DeclareForm,ChargeForm
from TripleMag.apps.store.models import stuff,order as my_order,order_stuff
from TripleMag.apps.member.models import user_max_mem,user_mid_mem,user_address,user_adder
from TripleMag.apps.money.models import store_declare_record
from TripleMag.apps.views import PaginatorFuc,CallProc,verify_password_2nd
import sys,threading

from Mall.engine.cart.cart_form.form import AddressForm

from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
@login_required    
@can_store_declare
@store_required
def index(request, **kwargs):
    """
    会员首页
    """
    template_name = "store/store_base.html"
    UserBasic = kwargs.pop("Mem")
    error=""
    if request.method == "POST":
    
        form = DeclareForm(request.POST,user = request.user)

        if form.is_valid():
            amount = form.cleaned_data['declare_style']
            UserBasic.store_order = UserBasic.store_order - Decimal(amount)
            #可能涉及奖金结算
            UserBasic.store_cash = UserBasic.store_cash + Decimal(amount)
            UserBasic.save()
            UserMaxMem = user_max_mem.objects.get(user_mid = user_mid_mem.objects.get(user = UserBasic) )
            StoreDeclareRecord = store_declare_record(max = UserMaxMem,amount = amount)
            StoreDeclareRecord.save()
    else:
        form = DeclareForm
    ctx ={
        'right':'store/declare.html',
        'UserBasic': UserBasic,
        'form':form
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
@login_required
@store_required
def charge(request, **kwargs):
    """
    报单中心充值
    """
    UserBasic = kwargs.pop("Mem")
    style = request.GET.get("style",None)
    amount = request.GET.get("amount",None)
    password_2nd = request.GET.get("password_2nd",None)
    result = verify_password_2nd(password_2nd,request.user)
    print result
    if result:
        try:
            amount = Decimal(amount)
            UserBasic.cash = UserBasic.cash - amount
            UserBasic.store_order  = UserBasic.store_order + amount
            UserBasic.save()
            data = '1'
        except:
            data = '0'
    else:
        data = '2'
    return HttpResponse(json.dumps(data),mimetype="application/json")
    
@login_required
@store_required
def declare_records(request, **kwargs):
    """
    查看报单记录
    """
    template_name = "store/store_base.html"
    UserBasic = kwargs.pop("Mem")
    UserMaxMem = user_max_mem.objects.filter(user_mid = user_mid_mem.objects.get(user = UserBasic) )
    StoreDeclareRecord = store_declare_record.objects.filter(max = UserMaxMem)
    
    StoreDeclareRecord = PaginatorFuc(request,StoreDeclareRecord)
    
    ctx = {
        'StoreDeclareRecords': StoreDeclareRecord,
        'right': 'store/delcare_records.html',
        'UserBasic': UserBasic
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))

@login_required
@admin_or_store_required
def added_mem(request, **kwargs):
    """
    查看自己添加的会员
    """
    template_name = kwargs.pop("template_name")
    right = "store/adder.html"
    UserBasic = kwargs.pop("Mem")
    UserAdder = user_adder.objects.filter(adding = UserBasic)
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT	BAS.number , BAS.name , LM.name ,MID.init_money ,  BAS.start_date FROM	`rtyk_triple`.`member_user_adder` AD INNER JOIN `rtyk_triple`.`member_user_mid_mem` MID ON MID.user_id = AD.added_id INNER JOIN `rtyk_triple`.`member_user_basic` BAS ON BAS.id = AD.added_id INNER JOIN `rtyk_triple`.`management_member_lv_money` LM ON LM.id = MID.level_id WHERE unix_timestamp(start_date) BETWEEN unix_timestamp(CURRENT_DATE - INTERVAL 3 MONTH) AND unix_timestamp(CURRENT_DATE)  and AD.adding_id = %s",UserBasic.id)
    adding_mem = cursor.fetchall()
    connection.close()
    cursor.close()
    
    adding_mem = PaginatorFuc(request,adding_mem,number=20)
#    print adding_mem
#    
#    if UserAdder:
#        for UAdder in UserAdder:
#            UserMidMem = user_mid_mem.objects.filter(user = UAdder.added)[0]
#            UAdder.level_name = UserMidMem.level.name
#            UAdder.money = UserMidMem.level.money
    
    ctx = {
        'UserBasic': UserBasic,
        'user_adder': adding_mem,
        'right': right,
        'user_number':UserBasic.number
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))
    
@store_required
def stuff_list(request, **kwargs):
    """
    查看货物列表
    """
    Stuff = stuff.objects.filter(total_num__gte=0).order_by("-id")
    template_name = "store/order.html"
    include_template = "store/stuff_table.html"
    UserBasic = kwargs.pop("Mem")
    
    Stuff = PaginatorFuc(request,Stuff,number=100)
    
    ctx = {
        "stuff": Stuff,
        "UserBasic": UserBasic,
        'include_template':include_template
    }
    return render_to_response(template_name, RequestContext(request, ctx))
    
@store_required
def stuff_info(request, **kwargs):
    """
    查看货物详情
    """
    stuff_id = request.GET.get("stuff_id",None)
    template_name = "store/stuff_info.html"
    if not stuff_id:
        raise Http404
    else:   
        Stuff = stuff.objects.get(id = stuff_id)
        
    ctx = {
        "Stuff": Stuff
    }
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
@store_required
def order(request, **kwargs):
    """
    生成订单
    """
    UserBasic = kwargs.pop("Mem")
    StuffList = request.GET.get("stuff_list",None)
    sum_price = 0
    print StuffList
    error = ""
    if StuffList:
        request.session['StuffList'] = StuffList
    
    template_name = "store/order.html"
    
    if request.method == "POST":
        if 'add_address' in request.POST:
            address = user_address(user = UserBasic)
            UserAddressForm = AddressForm(request.POST, instance=address) 
            print UserAddressForm
            if UserAddressForm.is_valid():
                UserAddressForm.save()
        elif 'order' in request.POST:
            
            password_2nd = request.POST.get("password_2nd")
            result = verify_password_2nd(password_2nd,request.user)

            if result:
                lock = threading.Lock()
                StuffList = request.session.get('StuffList')
                print StuffList
                address_id = request.POST.get("address_id")
                print address_id

                UserMaxMem = user_max_mem.objects.get(user_mid = user_mid_mem.objects.get(user = UserBasic))
                lock.acquire()
                try:
                    StuffList = StuffList.split("_")
                    success = False
                    x = 0
                    address = user_address.objects.get(id = address_id)
                    MyOrder = my_order(max = UserMaxMem,state = "wait",address = address)
                    MyOrder.save()
                    while x < len(StuffList)-1:
                        print x,StuffList
                        Stuff = stuff.objects.get(id = StuffList[x])
                        num = int(StuffList[x+1])
                        if Stuff.total_num >= num:
                            Stuff.total_num -=  num
                            price_total = Stuff.price_single * num
                            sum_price += price_total
                            UserBasic.store_cash -= Decimal(price_total)
                            UserBasic.save()
                            Stuff.save()
                            OrderStuff = order_stuff(order = MyOrder,stuff = Stuff,amount =num, price_total = price_total)
                            OrderStuff.save()
                            x += 2
                            success = True
                        else:
                            error += Stuff.name+"没有足够的数量,所以没有购买成功"
                    if success:
                        extra_context = UserBasic.number+"有新的订单"
                        admin = User.objects.filter(is_superuser = True)
                        notification.send(admin,"order_notice",extra_context,True, request.user)
                        url = reverse('stuff_order_records')+"?error="+error
                        return HttpResponseRedirect(url)
                finally:
                    lock.release()
            else:
                error = "二级密码错误"
    else:
        x = 0
        try:
            StuffList = StuffList.split("_")
            while x < len(StuffList)-1:
                print x,StuffList
                Stuff = stuff.objects.get(id = StuffList[x])
                num = int(StuffList[x+1])
                price_total = Stuff.price_single * num
                sum_price += price_total
                x += 2
            request.session['sum_price'] = sum_price
        except:
            print sum_price
        UserAddressForm = AddressForm
    UserAddress = user_address.objects.filter(user = UserBasic).order_by("-id")
    if not UserAddress:
        display = "block"
    else:
        display = "none"
    include_template = 'store/address.html'
    print error,'test'
    ctx = {
        'include_template':include_template,
        'UserAddress': UserAddress,
        'UserBasic': UserBasic,
        'display':display,
        'UserAddressForm':AddressForm,
        'sum_price':request.session.get('sum_price',0),
        "error":error
    }
    return render_to_response(template_name,RequestContext(request,ctx))
@login_required
def del_address(request, **kwargs):
    """
    删除地址
    """
    AddressId = request.GET.get("address_id")
    goto = request.GET.get("goto")
    try:
        UserAddress = user_address.objects.get(id = AddressId)
        UserAddress.delete()
    finally:
        if goto=="store":
            return HttpResponseRedirect(reverse('stuff_order'))
        elif goto == "mall":
            return HttpResponseRedirect(reverse('sure_to_pay'))
        elif goto=="address":
            return HttpResponseRedirect(reverse("manage_address"))
            
        
@login_required
@store_required
def address(request, **kwargs):
    """
    地址管理
    """
    UserBasic = kwargs.pop("Mem")
    
    if request.method == "POST":
        if 'add_address' in request.POST:
            address = user_address(user = UserBasic)
            UserAddress = AddressForm(request.POST, instance=address) 
            print UserAddress
            if UserAddress.is_valid():
                UserAddress.save()
        elif 'delete_address' in request.POST:
            print '222'
        elif 'change_address' in request.POST:
            print '333'
    else:
        UserAddress = AddressForm   
        include_template = 'store/add_address.html'
    template_name = 'store/order.html'
    ctx= {
        'UserBasic': UserBasic,
        'include_template': include_template,
        'UserAddress': UserAddress,
        'sum_price':request.session.get('sum_price',0)
    }
    return render_to_response(template_name,RequestContext(request, ctx))

@login_required
@admin_or_store_required
def store_order_records(request, **kwargs):
    """
    查看用户的订货记录
    """
    user = request.user
    StuffWaitOrder = {}
    Orders = {}
    error = request.GET.get("error","")
    UserBasic = kwargs.pop("Mem",None)
    include_template = "includes/stuff_order_records.html"
    if user.is_superuser or user.first_name=="finance":
        admin = True
        template_name = "management/member/store_order_records.html"
        
        if request.method == "POST":
            order_id = request.POST.get("order")
            Order = my_order.objects.get(id = order_id)
            UserBasic = Order.max.user_mid.user
            if 'cancle' in request.POST:
                Order.state = "deny"
                OrderStuff = order_stuff.objects.filter(order = Order)
                for OStuff in OrderStuff:
                    OStuff.stuff.total_num += OStuff.amount
                    UserBasic.store_cash += OStuff.price_total
                UserBasic.save()
            else:
                Order.state = "sure"
            Order.save()
        StuffOrder = my_order.objects.all().order_by("-id")
    else:
        admin = False
        template_name = "store/order.html"
        UserMaxMem = user_max_mem.objects.get(user_mid = user_mid_mem.objects.get(user = UserBasic))
        
        if request.method == "POST":
            order_id = request.POST.get("order")
            Order = my_order.objects.get(id = order_id)
            Order.state = "done"
            Order.save()
        StuffOrder = my_order.objects.filter(max = UserMaxMem)
    for so in StuffOrder:
        total_price = 0
        Stuff = order_stuff.objects.filter(order = so)
        for stuff in Stuff:
            total_price += stuff.price_total
        so.total_price = total_price
        so.wait = False
        so.sure = False
        if so.state == "wait" and user.is_superuser:
            so.wait = True
        elif so.state == "sure" and not user.is_superuser:
            so.sure = True
        so.Stuff = Stuff
    StuffOrder = PaginatorFuc(request,StuffOrder,number=5)
    
    
    
    ctx = {
        "stuff_order": StuffOrder,
        "admin": admin,
        'include_template':include_template,
        'UserBasic':UserBasic,
        'sum_price':request.session.get('sum_price',0),
        "error":error
    }
    
    return render_to_response(template_name, RequestContext(request,ctx))
        
