# -*- coding: utf8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 

from django.db import models
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError  
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.contrib.auth.models import User
from TripleMag.apps.member.models import user_basic,member_mid_upgrade_record,user_contactor,user_max_mem,user_mid_mem
from TripleMag.apps.store.models import stuff,stuff_type
from TripleMag.apps.decorators import admin_or_store_required
from TripleMag.apps.management.models import file_upload,value_setting
from django.forms import ModelForm
from TripleMag.apps.views import get_number
EnumMemberType=(
    ("MemMax","报单中心"),
    ("MemMid","会员"),
)
EnumContactedArea=(
    ("A","A区"),
    ("B","B区"),
)
EnumBankName=(
    ("NongHang","中国农业银行"),
    ("GongHang","中国工商银行"),
    ("ZhongHang","中国银行"),
    ("JianHang",'中国建设银行'),
    ("MinSheng",'中国民生银行'),
    ("YouZheng",'中国邮政储蓄'),
    ("JiaoTong",'交通银行'),
    ("ZhaoShang","招商银行 "),
)
class BasicForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.role = kwargs.pop("role",None)
        print self.role
        super(BasicForm, self).__init__(*args, **kwargs)
        
class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UserForm, self).__init__(*args, **kwargs)
        _number = get_number()
        self.fields['number'].initial = _number
    recommending = forms.CharField(
        label = _("推荐人编号"),
        widget = forms.TextInput(),
        max_length = 8,
        required = False,
    )
    number = forms.CharField(
        label = _("编号"),
#        initial = _number,
        widget = forms.TextInput()
    )
    password_1nd = forms.CharField(
        label = _("一级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    password_2nd = forms.CharField(
        label = _("二级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    password1_again = forms.CharField(
        label = _("一级密码确认"),
        widget = forms.PasswordInput(),
        required = True
    )
    password2_again = forms.CharField(
        label = _("二级密码确认"),
        widget = forms.PasswordInput(),
        required = True
    )
    role = forms.ChoiceField(
        label = _("类型"),
        widget = forms.Select(), 
        choices = EnumMemberType 
    )
    bank_name = forms.ChoiceField(
        label = _("开户银行"),
        choices = EnumBankName
        
    )
    proxy_area = forms.CharField(max_length=20,required=False,widget=forms.TextInput())
    proxy_city = forms.CharField(max_length=20,required=False,widget=forms.TextInput())
    proxy_province = forms.CharField(max_length=20,required=False,widget=forms.TextInput())
    class Meta:
        model = user_basic
        exclude = (
                      'user','start_date','is_stock_XR', 'is_blocked', 'cash', 
                      'store_order', 'store_cash', 'stock_repeat',
                      'stock_rebuy', 'stock_hold', 'mall_single_score',
                      'mall_team_score', 'store_total_money_A','store_total_money_B',
                      'sum_declare','sum_bonus_recost',
                      'stock_hold_0devide','stock_hold_1devide','stock_hold_2devide',
                      'can_devide','stock_hold_max','stock_sum','can_share_out','password_1nd'
                )
    def clean_bank_name(self):
        _name = self.cleaned_data['bank_name']
        for p in EnumBankName:
            if p[0] == _name:
                bank_name = p[1]
                print bank_name
        return bank_name
    def clean_recommending(self):
        recommending = self.cleaned_data['recommending']
        if not recommending:
            if not self.user.is_superuser:
                raise forms.ValidationError("推荐人不能为空")
        else:
            UserBasic = user_basic.objects.filter(number = recommending)
            if not UserBasic:
                raise forms.ValidationError("请输入正确的推荐人编号")
        return recommending
    def clean_password_2nd(self):
        password_2nd = self.cleaned_data['password_2nd']
        password_2nd = make_password(password_2nd)
        return password_2nd
        
class MemberForm(BasicForm):

    def get_level():
        level = []
        from TripleMag.apps.management.models import member_lv_money
        MemLevel = member_lv_money.objects.all()
        for ml in MemLevel:
            _level = []
            _level.append(ml.level)
            _level.append(ml.name)
            level.append(_level)
        return level
    contacting = forms.CharField(
        label=_("接点人编号"),
        max_length = 8,
        widget = forms.TextInput(),
        help_text = _("添加后不可修改"),
        required = False,
    )
    level = forms.ChoiceField(
        label = _("级别"),
        widget = forms.Select(), 
        choices = get_level(), 
        initial='1'
    )
    contact_area = forms.ChoiceField(
        label = _("所在区块"),
        widget = forms.Select(), 
        choices = EnumContactedArea, 
        initial='1'
    )
    style = forms.ChoiceField(
        label=_("报单中心类型"),
        widget = forms.Select(),
        choices = ([('1','社区店'),('2','中心店')]),
        required = False
    )
    proxy_style = forms.ChoiceField(
        label=_("代理中心类型"),
        widget = forms.Select(),
        choices = ([('1','无'),('2','区代'),('3','市代'),('4','省代')]),
        required = False
    )
    user_central = forms.CharField(
        label=_("填写中心店"),
        max_length = 8,
        widget = forms.TextInput(),
        help_text = _("添加后不可修改"),
        required = False,
    )
    def clean_contacting(self):
        contacting = self.cleaned_data['contacting']
        if not contacting:
            if not self.user.is_superuser:
                raise forms.ValidationError("接点人不能为空")
        else:
            UserBasic = user_basic.objects.filter(number = contacting)
            if not UserBasic:
                raise forms.ValidationError("请输入正确的接点人编号")
        return contacting
    def clean_contact_area(self):
        contacting = self.cleaned_data.get('contacting')
        contact_area = self.cleaned_data['contact_area']
        print contacting
        UserBasic = user_basic.objects.filter(number = contacting)
        if UserBasic:
            UserContactor = user_contactor.objects.filter(contacting = UserBasic[0],contact_area=contact_area)
            if UserContactor:
                error = '%s的%s区已经有接点人' % (contacting,contact_area)
                raise forms.ValidationError(error)
        return contact_area
    def clean_user_central(self):
        """
        判断是否是中心店
        """
        style = self.cleaned_data.get('style')
        user_central = self.cleaned_data['user_central']
        print self.cleaned_data.get('role')
        if user_central:
            if style == '1' and self.role=="MemMax":
                UserBasic = user_basic.objects.filter(number = user_central)
                if not UserBasic:
                    raise forms.ValidationError("会员不存在")
                else:
                    try:
                        UMax = user_max_mem.objects.filter(user_mid = user_mid_mem.objects.get(user = UserBasic[0]))[0]
                        if not UMax or not UMax.is_central: 
                            raise forms.ValidationError("该会员不是中心店")
                    except:
                        raise forms.ValidationError("该会员不是中心店")
        return user_central
        
class MemberUpgradeForm(BasicForm):
    #会员升级报单中心
    style = forms.ChoiceField(
        label=_("报单中心类型"),
        widget = forms.ChoiceField([('1','中心店'),('2','社区店')]),
        required = True
    )

class StuffTypeForm(ModelForm):
    """
    管理员添加货物类型表单
    """
    class Meta:
        model = stuff_type
        exclude = ('picture')
    
class StuffForm(ModelForm):
    """
    管理员添加货物表单GetNewRandomId
    """
    class Meta:
        model = stuff

class FileUploadForm(ModelForm):
    """
    资料上传表单
    """ 
    class Meta:
        model = file_upload
        exclude = ('time') 
        

class StockLockForm(BasicForm):
    """
    股票封闭期表单
    """
    stock_lock_start = forms.DateTimeField(widget=forms.TextInput(), label=u'开始时间')
    stock_lock_end = forms.DateTimeField(widget=forms.TextInput(), label=u'结束时间')

class StockAllOtMentForm(BasicForm):
    """
    拆股表单
    """
    rate = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required = True,
        widget = forms.TextInput()
    )
class StockSetValueForm(BasicForm):
    """
    设置当日价格
    """
    stock_value_now = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required = True,
        widget = forms.TextInput()
    )
    
class StockValuesForm(ModelForm):
    """
    股票设置表单
    """
    class Meta:
        model = value_setting
        fields = ('sell_min_amount','sell_max_amount','stock_tax_rate',
                  'stock_repo_rate','stock_ex_return_rate','stock_start_time','stock_end_time',
                  'stock_start_date','stock_end_date','stock_hold_max','P2P_radix','P2P_max',
                  'stock_selling_days','stock_share_out_min_amount','stock_value_now')
    
    
    def __init__(self,*args,**kwargs):
        self.value_setting = kwargs.pop("Value_Setting",None)
        super(StockValuesForm, self).__init__(*args, **kwargs)
    def clean_sell_min_amount(self):
        """
        设置股票的单次最少卖出股票数
        """
        sell_min_amount = self.cleaned_data['sell_min_amount']
        
        if sell_min_amount and sell_min_amount != self.value_setting.sell_min_amount:
            self.value_setting.sell_min_amount = sell_min_amount
            self.value_setting.save()
        return sell_min_amount
        
    def clean_sell_max_amount(self):
        """
        设置股票的单次最多卖出股票数
        """
        sell_max_amount = self.cleaned_data['sell_max_amount']
        
        if sell_max_amount and sell_max_amount != self.value_setting.sell_max_amount:
            self.value_setting.sell_max_amount = sell_max_amount
            self.value_setting.save()
    def clean_stock_tax_rate(self):
        """
        设置股票的抽税比例
        """
        stock_tax_rate = self.cleaned_data['stock_tax_rate']
        
        if stock_tax_rate and stock_tax_rate != self.value_setting.stock_tax_rate:
            print stock_tax_rate,'test'
            self.value_setting.stock_tax_rate = stock_tax_rate
            print self.value_setting.stock_tax_rate ,'test'
            self.value_setting.save()
    
    def clean_stock_value_now(self):
        stock_value_now = self.cleaned_data['stock_value_now']
        if stock_value_now and self.value_setting.stock_value_now != stock_value_now:
            self.value_setting.stock_value_now = stock_value_now
            self.value_setting.save()
    
    def clean_stock_repo_rate(self):
        """
        设置股票的回购比例
        """
        stock_repo_rate = self.cleaned_data['stock_repo_rate']
        if stock_repo_rate and stock_repo_rate != self.value_setting.stock_repo_rate:
            self.value_setting.stock_repo_rate = stock_repo_rate
            self.value_setting.save()
    def clean_stock_ex_return_rate(self):
        """
        设置股票返给上级的比例
        """
        stock_ex_return_rate = self.cleaned_data['stock_ex_return_rate']
        if stock_ex_return_rate and stock_ex_return_rate != self.value_setting.stock_ex_return_rate:
            self.value_setting.stock_ex_return_rate = stock_ex_return_rate
            self.value_setting.save()
    def clean_stock_start_time(self):
        """
        设置股票的开始时间
        """
        stock_start_time = self.cleaned_data['stock_start_time']
        
        if stock_start_time and self.value_setting.stock_start_time != stock_start_time:
            self.value_setting.stock_start_time = stock_start_time
            print self.value_setting.stock_start_time,'sssssssssss'
            print type(self.value_setting.stock_start_time)
            self.value_setting.save()
            
    def clean_stock_end_time(self):
        """
        设置股票的结束时间
        """
        stock_end_time = self.cleaned_data['stock_end_time']
        if stock_end_time and self.value_setting.stock_end_time != stock_end_time:
            self.value_setting.stock_end_time = stock_end_time
            self.value_setting.save()
    def clean_stock_selling_days(self):
        """
        设置股票的持续时间
        """
        stock_selling_days = self.cleaned_data['stock_selling_days']
        if stock_selling_days and self.value_setting.stock_selling_days != stock_selling_days:
            print type(stock_selling_days),'jjjjjjjjjjjj'
            self.value_setting.stock_selling_days = stock_selling_days
            self.value_setting.save()
    def clean_stock_start_date(self):
        """
        设置股票的开始日期
        """
        stock_start_date = self.cleaned_data['stock_start_date']
        if stock_start_date and self.value_setting.stock_start_date != stock_start_date:
            self.value_setting.stock_start_date = stock_start_date
            print type(stock_start_date),'hhhhhhh'
            self.value_setting.save()
        
    def clean_stock_end_date(self):
        """
        设置股票的结束日期
        """
        stock_end_date = self.cleaned_data['stock_end_date']
        if stock_end_date and self.value_setting.stock_end_date != stock_end_date:
            self.value_setting.stock_end_date = stock_end_date
            self.value_setting.save()
    def clean_stock_hold_max(self):
        """
        设置股票的最大持有拆股数
        """
        stock_hold_max = self.cleaned_data['stock_hold_max']
        if stock_hold_max and stock_hold_max != self.value_setting.stock_hold_max:
            self.value_setting.stock_hold_max = stock_hold_max
            self.value_setting.save()
    def clean_P2P_radix(self):
        """
        设置点对点的股票卖出基数
        """
        P2P_radix = self.cleaned_data['P2P_radix']
        if P2P_radix and P2P_radix!=self.value_setting.P2P_radix:
            self.value_setting.P2P_radix = P2P_radix
            self.value_setting.save()
    def clean_P2P_max(self):
        """
        设置点对点的股票的最大卖出数
        """
        P2P_max = self.cleaned_data['P2P_max']
        
        if P2P_max and P2P_max != self.value_setting.P2P_max:
            self.value_setting.P2P_max = P2P_max
            self.value_setting.save()
    def clean_stock_share_out_min_amount(self):
        """
        参与分红股票最小值
        """
        stock_share_out_min_amount = self.cleaned_data['stock_share_out_min_amount']
        
        if stock_share_out_min_amount and stock_share_out_min_amount != self.value_setting.stock_share_out_min_amount:
            self.value_setting.stock_share_out_min_amount = stock_share_out_min_amount
            self.value_setting.save()
    def save(self):
        
        print self.value_setting,'test'
        print self.value_setting.stock_tax_rate, 'test'
        return self.value_setting
        
class CWebValueSettingForm(ModelForm):
    """
    C网奖金设定表单
    """
    
    class Meta:
        model = value_setting
        fields = ("grade_summit",'mall_VIP_threshold','mall_love_rate','mall_car_rate',
                 'mall_house_rate','mall_travel_rate','mall_share_rate',
                 'mall_proxy_rate','mall_recommend_rate','mall_proxy_prov',
                 'mall_proxy_city','mall_proxy_area','mall_tax_rate')
        
    def __init__(self,*args, **kwargs):
        self.ValueSetting = kwargs.pop("ValueSetting",None)
        print self.ValueSetting,'test'
        super(CWebValueSettingForm, self).__init__(*args, **kwargs)
    def clean(self):
        grade_summit = self.cleaned_data.get('grade_summit')
        mall_VIP_threshold = self.cleaned_data.get('mall_VIP_threshold')
        mall_love_rate = self.cleaned_data.get('mall_love_rate')
        mall_car_rate = self.cleaned_data.get('mall_car_rate')
        mall_house_rate = self.cleaned_data.get('mall_house_rate')
        mall_travel_rate = self.cleaned_data.get('mall_travel_rate')
        mall_share_rate = self.cleaned_data.get('mall_share_rate')
        mall_proxy_rate = self.cleaned_data.get('mall_proxy_rate')
        mall_recommend_rate = self.cleaned_data.get('mall_recommend_rate')
        mall_proxy_prov = self.cleaned_data.get('mall_proxy_prov')
        mall_proxy_city = self.cleaned_data.get('mall_proxy_city')
        mall_proxy_area = self.cleaned_data.get('mall_proxy_area')
        mall_tax_rate = self.cleaned_data.get("mall_tax_rate")
        print mall_tax_rate,'kkkkk'
        if grade_summit and self.ValueSetting.grade_summit != grade_summit:
            self.ValueSetting.grade_summit = grade_summit
        if mall_VIP_threshold and self.ValueSetting.mall_VIP_threshold != mall_VIP_threshold:
            self.ValueSetting.mall_VIP_threshold = mall_VIP_threshold
        if mall_love_rate and self.ValueSetting.mall_love_rate != mall_love_rate:
            self.ValueSetting.mall_love_rate = mall_love_rate
        if mall_car_rate and self.ValueSetting.mall_car_rate != mall_car_rate:
            self.ValueSetting.mall_car_rate = mall_car_rate
        if mall_house_rate and self.ValueSetting.mall_house_rate != mall_house_rate:
            self.ValueSetting.mall_house_rate = mall_house_rate
        if mall_travel_rate and self.ValueSetting.mall_travel_rate != mall_travel_rate:
            self.ValueSetting.mall_travel_rate = mall_travel_rate
        if mall_share_rate and self.ValueSetting.mall_share_rate != mall_share_rate:
            self.ValueSetting.mall_share_rate = mall_share_rate
        if mall_proxy_rate and self.ValueSetting.mall_proxy_rate != mall_proxy_rate:
            self.ValueSetting.mall_proxy_rate = mall_proxy_rate
        if mall_recommend_rate and self.ValueSetting.mall_recommend_rate != mall_recommend_rate:
            self.ValueSetting.mall_recommend_rate = mall_recommend_rate
        if mall_proxy_prov and self.ValueSetting.mall_proxy_prov != mall_proxy_prov:
            self.ValueSetting.mall_proxy_prov = mall_proxy_prov
        if mall_proxy_city and  self.ValueSetting.mall_proxy_city != mall_proxy_city:
            self.ValueSetting.mall_proxy_city = mall_proxy_city
        if mall_proxy_area and self.ValueSetting.mall_proxy_area != mall_proxy_area:
            self.ValueSetting.mall_proxy_area = mall_proxy_area
        if mall_tax_rate and self.ValueSetting.mall_tax_rate != mall_tax_rate:
            self.ValueSetting.mall_tax_rate = mall_tax_rate
        self.ValueSetting.save()
        return self.cleaned_data

class AWebValueSettingForm(ModelForm):
    """
    产品销售数值设定表单
    """
    class Meta:
        model = value_setting
        fields = ("password_1nd",'password_2nd','withdraw_rate','declare_central_rate',
                    'declare_normal_rate','bonus_tax_rate','repo_rate','recost_rate',
                    'comhelp_rate','comhelp_1st_min','comhelp_2nd_min',
                    'comhelp_3rd_min',)
                    
    def __init__(self,*args, **kwargs):
        self.ValueSetting = kwargs.pop("ValueSetting",None)
        print self.ValueSetting,'test'
        super(AWebValueSettingForm, self).__init__(*args, **kwargs)
    def clean(self):
        password_1nd = self.cleaned_data.get("password_1nd")
        password_2nd =  self.cleaned_data.get('password_2nd')
        withdraw_rate = self.cleaned_data.get('withdraw_rate')
        declare_central_rate = self.cleaned_data.get('declare_central_rate')
        declare_normal_rate = self.cleaned_data.get('declare_normal_rate')
        bonus_tax_rate = self.cleaned_data.get('bonus_tax_rate')
        repo_rate = self.cleaned_data.get("repo_rate")
        recost_rate =  self.cleaned_data.get("recost_rate")
        comhelp_rate =  self.cleaned_data.get("comhelp_rate")
        comhelp_1st_min = self.cleaned_data.get("comhelp_1st_min")
        comhelp_2nd_min = self.cleaned_data.get('comhelp_2nd_min')
        comhelp_3rd_min = self.cleaned_data.get("comhelp_3rd_min")
        print comhelp_1st_min,comhelp_2nd_min,comhelp_3rd_min
        if password_1nd and self.ValueSetting.password_1nd != password_1nd:
            self.ValueSetting.password_1nd = password_1nd 
        if password_2nd and self.ValueSetting.password_2nd != password_2nd:
            self.ValueSetting.password_2nd = password_2nd
        if withdraw_rate and self.ValueSetting.withdraw_rate != withdraw_rate:
            self.ValueSetting.withdraw_rate = withdraw_rate
        if declare_central_rate and self.ValueSetting.declare_central_rate != declare_central_rate:
            self.ValueSetting.declare_central_rate = declare_central_rate
        if declare_normal_rate and self.ValueSetting.declare_normal_rate != declare_normal_rate:
            self.ValueSetting.declare_normal_rate = declare_normal_rate
        if bonus_tax_rate and bonus_tax_rate != self.ValueSetting.bonus_tax_rate:
            self.ValueSetting.bonus_tax_rate = bonus_tax_rate 
        if repo_rate and self.ValueSetting.repo_rate != repo_rate:
            self.ValueSetting.repo_rate = repo_rate
        if recost_rate and self.ValueSetting.recost_rate != recost_rate:
            self.ValueSetting.recost_rate = recost_rate
        if comhelp_rate and self.ValueSetting.comhelp_rate!=comhelp_rate:
            self.ValueSetting.comhelp_rate = comhelp_rate
        if comhelp_1st_min and self.ValueSetting.comhelp_1st_min != comhelp_1st_min:
            self.ValueSetting.comhelp_1st_min = comhelp_1st_min
        if comhelp_2nd_min and self.ValueSetting.comhelp_2nd_min != comhelp_2nd_min:
            self.ValueSetting.comhelp_2nd_min = comhelp_2nd_min
        if comhelp_3rd_min and self.ValueSetting.comhelp_3rd_min != comhelp_3rd_min:
            self.ValueSetting.comhelp_3rd_min = comhelp_3rd_min
        self.ValueSetting.save()     
        return self.cleaned_data        

class Password1stForm(forms.Form):
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop("user",None)
        print self.user
        super(Password1stForm, self).__init__(*args, **kwargs)

    password_1st = forms.CharField(
        label = _("一级密码"),
        widget = forms.PasswordInput(),
        required = True
    )
    
    def clean_password_1st(self):
        password_1nd = self.cleaned_data['password_1st']
        result = self.user.check_password(password_1nd)
        print password_1nd,'hhhh'
        print result
        if not result:
            raise forms.ValidationError("你的密码错误")
        return password_1nd
