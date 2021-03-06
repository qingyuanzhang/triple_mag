# -*- coding: utf8 -*-
import sys,threading
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
from django.db.models import Q,F
from django.shortcuts import render_to_response,HttpResponseRedirect,RequestContext,HttpResponse,render
from TripleMag.apps.decorators import store_required,mem_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decimal import *
from django.http import Http404
from django.contrib.auth.models import User
from django.http import Http404
from django.template import RequestContext,loader
import json 
from django.core.urlresolvers import reverse
from TripleMag.apps.decorators import get_user_basic,store_required,admin_required,can_member_register
from TripleMag.apps.mall.forms import *
from TripleMag.apps.mall.models import *
from TripleMag.apps.store.models import stuff,order as my_order,order_stuff
from TripleMag.apps.member.models import user_max_mem,user_mid_mem,user_basic,user_recommender
from TripleMag.apps.management.forms import UserForm
from TripleMag.apps.views import CallProc
from django.db import connection
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from TripleMag.apps.management.models import notice_mall
from TripleMag.apps.mall.forms import MallIndexForm,MallAdForm,NoticeMallForm

from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
@login_required    
@admin_required    
def index(request, **kwargs):
    """
    商城管理首页
    """
    template_name = kwargs.pop("template_name")

    
    return render(request,template_name)
    
@login_required
@admin_required
def category_index(request, **kwargs):
    """
    目录首页
    """
    template_name = kwargs.pop("template_name",None)
    category_1st = Category.objects.all()
    category_2nd = CategoryFirst.objects.all()
    category_3rd = CategorySecond.objects.all()
    
    if request.method == "POST":
        if 'category' in request.POST:
            category_form = CategoryForm(request.POST,request.FILES)
            if category_form.is_valid():
                category_form.save()
                reset_category(request)
                return HttpResponseRedirect(reverse("mall_category_index"))
        elif 'category_first' in request.POST:
            category_first_form = CategoryFirstForm(request.POST,request.FILES)
            if category_first_form.is_valid():
                category_first_form.save()
                reset_category(request)
                return HttpResponseRedirect(reverse("mall_category_index"))
        elif 'category_second' in request.POST:
            category_second_form = CategorySecondForm(request.POST,request.FILES)
            if category_second_form.is_valid(): 
                category_second_form.save()
                reset_category(request)
                
                return HttpResponseRedirect(reverse("mall_category_index"))
    category_form = CategoryForm
    category_first_form = CategoryFirstForm
    category_second_form = CategorySecondForm
    ctx = {
        'category_1st': category_1st,
        'category_2nd': category_2nd,
        'category_3rd':category_3rd,
        'CategoryForm':category_form,
        'CategoryFirstForm': category_first_form,
        'CategorySecondForm':category_second_form,
    }
    
    
    return render_to_response(template_name,RequestContext(request,ctx))
def reset_category(request):
    category = Category.objects.all()[0:10]
    for ct1 in category:
        category_2 = CategoryFirst.objects.filter(father_catagory = ct1.id);#第2层目录
        ct1.ct2 = category_2
        for ct2 in ct1.ct2:
            category_3 = CategorySecond.objects.filter(father_catagory = ct2)
            ct2.ct3 = category_3
    request.session['category'] = category
@login_required
@admin_required
def delete_category(request,c_id=None,model=None,p_id=None, **kwargs):
    """
    删除目录
    """
    if c_id:
        delete_id = c_id
        url = reverse("mall_category_index")
    elif p_id:
        delete_id = p_id
        url = reverse("product_list")
    try:
        
        Model = model.objects.get(id = delete_id)
        print 'ssss'
        Model.delete()
        
        reset_category(request)
        return HttpResponseRedirect(url)
    except:
        raise Http404
    

def manage_product(request, **kwargs):
    """
    管理商品和目录
    """
    template_name = "management/mall/product.html"
    product_id = request.GET.get("p_id")
    product = ""
    image_url = ""
    MallProdCombn = ""
    if request.method == "POST":
        if 'product' in request.POST:
            product_form = ProductForm(request.POST,request.FILES)

            if product_form.is_valid():
                recommender = user_basic.objects.filter(number = product_form.cleaned_data['recommender'])[0]
                try:
                    product = Product.objects.get(id = product_id)
                    product.recommender = recommender
                except:
                    product = Product(recommender = recommender)
                try:
                    ProductImage = product_image.objects.filter(product = product)
                    ProductImage.delete()
                except:
                    pass
                product_form = ProductForm(request.POST,request.FILES,instance=product)
                product_form.save()
                image_url = request.POST.getlist("product_image",None)
                if image_url:
                    for image in image_url:
                        if image:
                            ProductImage = product_image(image_url = image,product=product)
                            ProductImage.save()
                
                color = request.POST.getlist("color")
                size = request.POST.getlist("size")
                if color or size:
                    MallProdCombn =  mall_prod_combination.objects.filter(product = product)
                    if MallProdCombn:
                        MallProdCombn.delete()
                    
                    for i in range(0,len(color)):
                        MallProdCombn = mall_prod_combination(product = product,size = size[i],color=color[i])
                        MallProdCombn.save()
                return HttpResponseRedirect(reverse("manage_product"))
#        
#                except:
#                    error="用户不存在"
    else:
        try:
            product = Product.objects.get(id = product_id)
            MallProdCombn = mall_prod_combination.objects.filter(product = product)
            product_form = ProductForm(instance = product)
            image_url = product_image.objects.filter(product = product)
            print image_url
        except:
            product_form = ProductForm
    ctx = {
        'ProductForm':product_form,
        'p_id':product_id,
        'product':product,
        'image_url':image_url,
        'MallProdCombn':MallProdCombn
    }
    return render_to_response(template_name, RequestContext(request,ctx))
def category(request ,**kwargs):
    """
    目录管理
    """
    style = kwargs.pop("style")
    template_name = "mall/category.html"
    if request.method == "POST":
        if style == '1':
            form = CategoryForm(request.POST,request.FILES)
            print form
        elif style == '2':
            form = CategoryFirstForm(request.POST,request.FILES)
        elif style == '3':
            form = CategorySecondForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form_list = {
            '1': CategoryForm(),
            '2': CategoryFirstForm(),
            '3': CategorySecondForm()
        }
        if style == '1':
            model = Category.objects.all().order_by("-id")
        elif style == '2':
            model = CategoryFirst.objects.all().order_by("-id")            
        elif style == '3':
            model = CategorySecond.objects.all().order_by("-id")
        form = form_list[style]

    ctx={
        'form': form,
        'model': model
    }
     
    return render_to_response(template_name,RequestContext(request, ctx))


@login_required
def mall_collection(request, **kwargs):
    """
    收藏商品
    """
    print 'ss'
    user = request.user
    data = '收藏失败'
    if user.is_superuser:
        data =  '收藏失败'
    else:
        
        product_id = request.GET.get('p_id')
        print product_id
        product = Product.objects.get(id = product_id)
        UserBasic = user_basic.objects.filter(user = user)[0]
        collection = Collection.objects.filter(user = UserBasic,product=product)
        
        if collection:
            data="你已经收藏过该商品"
        else:
            try:
                
                collection = Collection.objects.create(user = UserBasic,product=product)
                data="收藏成功"
            except:
                data = "收藏失败"
    
    return HttpResponse(json.dumps(data),mimetype="application/json")

@can_member_register
def register(request, **kwargs):
    """
    用户注册
    """
    template_name = "mall/register.html"
    nextURL =request.GET.get('nextURL','/')
    
    error=""
    form = RegisterForm
    if request.method == "POST":
        error = save_user(request)
        if not error:
            return HttpResponseRedirect(nextURL)

    ctx = {
        'form': form,
        'error':error
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
    
def save_user(request):
    import random
    number = request.POST.get('number')
    name = request.POST.get('name')
    password_1nd = request.POST.get('password_1nd')
    password_2nd = make_password(request.POST.get('password_2nd'))
    recommender = request.POST.get('recommender')
    error = ""
    try:
        Recommender = user_basic.objects.defer(None).filter(number = recommender)[0]
    except:
        cursor = connection.cursor()  
        cursor.execute("select * from V_REC_ROOTS") 
        result = random.choice(cursor.fetchall())
        Recommender = user_basic.objects.defer(None).get(id = result[0])
    gender = request.POST.get('gender')
    phone = request.POST.get('phone')
    mobile = request.POST.get('mobile')
    QQ = request.POST.get('QQ')
    if not QQ:
        QQ = "无"
    if not phone:
        phone ="无"
    if not mobile:
        mobile="无"
    proxy_province = request.POST.get('proxy_province')
    proxy_city = request.POST.get('proxy_city')
    proxy_area = request.POST.get('proxy_area')
    try:
        user = User.objects.create_user(number, "",password_1nd)
        UserBasic = user_basic.objects.create(user = user,is_void=False,role="MemMin",number = number,name=name,password_1nd=user.password,password_2nd=password_2nd,gender=gender,mobile=mobile,QQ=QQ,phone=phone,proxy_province=proxy_province,
        proxy_city= proxy_city,proxy_area=proxy_area,bank_name="",bank_account_name="",bank_account_id=""
        )
        UserRecommender = user_recommender()
        UserRecommender.recommended = UserBasic
        UserRecommender.recommending = Recommender
        UserRecommender.save()
        user = authenticate(username=number,password=password_1nd)
        login(request,user)
    except:
        error="用户已经存在,请换一个号码"

    return error
@login_required

def order_management(request, **kwargs):
    """
    订单发货管理
    """
    user = request.user
    order_status = request.GET.get('order_status',None)
    order_id = request.GET.get('order_id',None)
    try:
        order = Order.objects.get(id = order_id)
    except:
        return HttpResponseRedirect('/mall/user/my_order/?page=1')
    if user.is_superuser:
        if order_status == 'cancle':
            order.delete()
        elif order_status == "wait" and order.status=="wait":
            dlivery_number = request.POST.get("dlivery_way")
            dlivery_way = request.POST.get("dlivery_number")
            order.transport_ways = dlivery_way+"@"+dlivery_number
            order.status = 'sent'
            
    else:
        if order_status == "sent" and order.status == "sent":
            order.status = "finish"
            call_proc = CallProc()
            proc_name = "mall_purchase"
            call_proc.CallProcFuc_1(proc_name,order.id)
    order.save()
    return HttpResponseRedirect('/mall/user/my_order/?page=1')
    
@login_required
def change_password(request,**kwargs):
    """
    修改密码
    """
    if request.user.is_superuser or request.user.first_name == "finance":
        UserBasic = None
    else:
        try:
            UserBasic = user_basic.objects.defer("password_1nd","password_2nd").filter(user = request.user)[0]
        except:
            raise Http404
    template_name = "mall/change_password.html"
    change_password_form = ""
    change_password_2nd_form = ""
    if request.method == "POST":
        if "change_password_form" in request.POST:
            change_password_form = ChangePasswordForm(request.POST,user = request.user,UserBasic = UserBasic)
            if change_password_form.is_valid():
                return HttpResponseRedirect("/")
        elif "change_password_2nd_form" in request.POST:
            change_password_2nd_form = ChangePassword_2ndForm(request.POST,user = request.user,UserBasic = UserBasic)
            if change_password_2nd_form.is_valid():
                return HttpResponseRedirect("/")
    else:
        change_password_form = ChangePasswordForm()
        change_password_2nd_form = ChangePassword_2ndForm()
    ctx = {
        'change_password_form':change_password_form,
        'change_password_2nd_form':change_password_2nd_form
    }
    return render_to_response(template_name,RequestContext(request,ctx))

@login_required
def my_collections(request,**kwargs):
    """
    收藏商品界面
    """
    template_name = "mall/collections.html"
    c_id =request.GET.get("c_id")
    try:
        UserBasic = user_basic.objects.defer(None).get(user = request.user)
    except:
        raise Http404
    collections = Collection.objects.filter(user = UserBasic)
    if c_id:
        
        try:
            _collection = collections.get(id = c_id)
            _collection.delete()
        except:
            print 'dd'
    ctx = {
        "collections":collections
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
    
@login_required
@admin_required
def product_list(request, **kwargs):
    """
    商品列表
    """
    template_name = kwargs.pop("template_name")
    products = Product.objects.all().order_by("-id")
    for product in products:
        print product
        try:
            product.catagroy = product.father_catagory.father_catagory.father_catagory.name
        except:
            product.catagroy = "无"
        try:
            product.catagroy1 = product.father_catagory.father_catagory.name
        except:
            product.catagroy1 = "无"
        try:
            product.catagroy2 = product.father_catagory.name
        except:
            product.catagroy2 = "无"
    ctx = {
        "products":products
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
@login_required
@admin_required
def mall_home_mag(request,model=None,form=None,del_id=None,**kwargs):
    """
    商城主页设置
    """    
    template_name = kwargs.pop("template_name")
    ResultList = model.objects.all().order_by("-id")
    print ResultList
    if del_id:
        try:
            DelModel = model.objects.get(id = del_id)
            DelModel.delete()
        except:
            print 'ss'
    ctx = {
        "Result":ResultList,
        "form":form
    }
    return render_to_response(template_name,RequestContext(request,ctx))

@login_required
@admin_required
def change_mall_announcement(request,**kwargs):
    """
    修改商城公告
    """
    template_name = "management/mall/mall_new_Announcement.html"
    a_id = request.GET.get("a_id")
    try:
        NoticeMall = notice_mall.objects.get(id = a_id)
    except:
        raise Http404
    
    if request.method == "POST":
        form = NoticeMallForm(request.POST,request.FILES,instance=NoticeMall)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/mall_notice/")
    else:
        form = NoticeMallForm(instance = NoticeMall)
        
    ctx = {
        "form":form,
        'change':True,
        'a_id':a_id
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
    
    
#@login_required
#@admin_required
#def management_mall_add(request, **kwargs):
#    """
#    商城推广设置
#    """
#    template_name = "management/mall/mall_ad.html"
#    
#    MallAdd = mall_ad.objects.all()
#    
#    ctx = {
#        "management_mall_ad":MallAdd
#    }
#    
#    return render_to_response(template_name,RequestContext(request,ctx))
#    
#@login_required
#@admin_required
#def management_mall_notice(request, **kwargs):
#    """
#    商城公告设置
#    """
#    NoticeMall = notice_mall.objects.all()
#    
#    template_name = "mall"
    
@login_required
@admin_required
def add_home_mag(request,**kwargs):
    """
    添加商城首页图片
    """
    template_name = "management/mall/mall_home_mag.html"
    form = MallIndexForm(request.POST,request.FILES)
    if form.is_valid():
        
        form.save()
        return HttpResponseRedirect("/mall_home_mag/")

    ctx = {
        "form":form
    }    
    return render_to_response(template_name,RequestContext(request,ctx))
@login_required
@admin_required
def add_mall_ad(request, **kwargs):
    """
    添加商城推广
    """
    template_name = "management/mall/mall_ad.html"
    form = MallAdForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        
        return HttpResponseRedirect("/mall_ad/")
    ctx = {
        "form":form
    }
    return render_to_response(template_name,RequestContext(request,ctx))
    
@login_required
@admin_required
def add_mall_notice(request, **kwargs):
    """
    添加商城公告
    """
    template_name = "management/mall/mall_new_Announcement.html"
    form = NoticeMallForm(request.POST,request.FILES)

    if form.is_valid():
        form.save()
        
        return HttpResponseRedirect("/mall_notice/")
    
    ctx = {
        'form':form
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))
@login_required
def comment(request, **kwargs):
    """
    评价商品
    """
    shop_record_id = kwargs.pop("shop_record_id",None)
    if not shop_record_id:
        raise Http404
    else:
        try:
            ShopRecord = shop_record.objects.get(id = shop_record_id)
            evalue_num = request.GET.get("evalue_num")
            evaluation = request.GET.get("evaluation")
	    try:
                ShopRecord.evaluation += evaluation
            except:
            	ShopRecord.evaluation = evaluation
            ShopRecord.evaluation += evaluation
            ShopRecord.evalue_num = evalue_num
            ShopRecord.save()
            return HttpResponseRedirect(reverse("user_account_my_order"))
        except:
            raise Http404
def search(request, **kwargs):
    """
    商品
    """
    keywords = request.GET.get("keywords",None)
    brand = request.GET.get("brand",None)
    sprice = request.GET.get("sprice",None)
    eprice = request.GET.get("eprice",None)
    spv = request.GET.get("spv",None)
    epv = request.GET.get("epv",None)
    sort = request.GET.get("sort",None)
    products = ""
    sql = ""
    full_url = request.get_full_path()
    brands = []
    full_url = full_url.split("&")
    pv_url= full_url[0]
    brand_url = full_url[0]
    price_url =full_url[0]
    sort_url = full_url[0]
    for i in range(1,len(full_url)):
        if full_url[i].find("sprice")== -1 and full_url[i].find("eprice")==-1:
            price_url +="&"+full_url[i]
        if full_url[i].find("spv")== -1 and full_url[i].find("epv")== -1:
            pv_url += "&"+full_url[i]
        if full_url[i].find("brand")==-1:
            brand_url += "&"+full_url[i]
        if full_url[i].find("sort") == -1:
            sort_url += "&"+full_url[i]
    products = Product.objects.filter(Q(name__icontains = keywords) | Q(brand__icontains = keywords) | Q(details__icontains =keywords))
    
    if sprice:
        if not eprice:  
            products = products.filter(price_VIP__gte = sprice)
        else:
            products = products.filter(price_VIP__range=(sprice,eprice))
    if spv:
        if not epv:
            products = products.filter(grade__gte = spv)
        else:
            products = products.filter(grade__range = (spv,epv))
    if brand:
        products = products.filter(brand = brand)
    try:
        _sort = sort.split("*")
        st = ""
        if _sort[1]=='0':
            st ="-"+_sort[0]
        else:
            st = _sort[0]
        products = products.order_by(st)
    
    except:
        print 'kkk'
    for product in products:
        brands.append(product.brand)
        
    
    
    brands = list(set(brands))
    template_name = "mall/search.html"
    ctx = {
        "products":products,
        'pv_url':pv_url,
        "brand_url":brand_url,
        'price_url':price_url,
        "sort_url":sort_url,
        "brands":brands,
        "sort":sort
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))
    
def mall_notice(request, **kwargs):
    """
    商城公告
    """
    n_id = request.GET.get("n_id")
    
    try:
        NoticeMall = notice_mall.objects.get(id = n_id)
    except:
        raise Http404
    
    template_name = "mall/notice.html"
    ctx = {
        "NoticeMall":NoticeMall
    }
    
    return render_to_response(template_name,RequestContext(request,ctx))
    
@login_required
def cancle_order(request, **kwargs):
    """
    会员取消订单
    """
    order_id = request.GET.get("order_id")
    print order_id
    order = Order.objects.get(id = order_id)

    order.delete()

    return HttpResponseRedirect(reverse("user_account_my_order"))
        
@login_required
@admin_required
def change_category(request, **kwargs):
    """
    修改目录
    """
    category = request.GET.get("category")
    c_id = request.GET.get("c_id")
    new_category = request.GET.get("new_category")
    result = ""
    try:
        if category == "ct1":
            category = Category.objects.get(id = c_id)
        elif category == "ct2":
            category = CategoryFirst.objects.get(id = c_id)
        elif category == "ct3":
            category = CategorySecond.objects.get(id = c_id)
        category.name = new_category
        category.save()
        result = "1"
        reset_category(request)
    except:
        result = "0"
    
    return HttpResponse(json.dumps(result),mimetype="application/json")
        
    
    
    
