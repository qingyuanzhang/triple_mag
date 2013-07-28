// JavaScript Document
$(document).ready(function()
{
	$.tools.validator.localize("cn", {
		'*'			: '抱歉，您的表单有错误。',
		':email'  	: '错误的邮箱',
		':number' 	: '请输入正确的数字',
		':url' 		: 'URL输入错误',
		'[max]'	 	: '这个数字不能大于 $1',
		'[min]'		: '这个数字不能小于 $1',
		'[required]'	: '请填写这个字段'
	});
});

$.tools.validator.fn("[name=username]", {"cn":'请输入用户名'} , function (input, value) {
		return value.length > 0 ;
});

$.tools.validator.fn("[name=password]", {"cn":'请输入的密码'} , function (input, value) {
		return value.length > 0 ;
});

/*$.tools.validator.fn("[name=captcha_1]", {"cn":'请输入正确的验证码'} , function (input, value) {
		return value.length == 4 ;
});*/
	
$.tools.validator.fn("[name=phone]", {"cn":'请输入正确的固定电话'} , function (input, value) {
	return /\d{6}\d*$/.test(value) || value.length == 0 ;
});

$.tools.validator.fn("[name=mobile],[name=contact_mobile]", {"cn":'请输入正确的手机号码'} , function (input, value) {
	return /\d{6}\d*$/.test(value) || value.length == 0 ;
});

$.tools.validator.fn("[name=QQ]", {"cn":'请输入正确的QQ号'} , function (input, value) {
	return /[1-9]\d{4,10}/.test(value) || value.length == 0 ;
});

$.tools.validator.fn("[name=bank_account_name]", {"cn":'请输入开户人中文姓名'} , function (input, value) {
	return /^[\u4e00-\u9fa5]+$/.test(value) ;
});
/*
//由于推荐人和接点人最初都有不符合编号的情形，因此先不显示
$.tools.validator.fn("[name=recommending]", {"cn":'请输入正确的推荐人编号'} , function (input, value) {
	return /^RT\d+/.test(value) && value.length == 8 ;
});
$.tools.validator.fn("[name=contacting]", {"cn":'请输入正确的接点人编号'} , function (input, value) {
	return /^RT\d+/.test(value) && value.length == 8 ;
});
*/
$.tools.validator.fn("[name=password_1nd],[name=password1_again]", {"cn":'$1'} , function (input, value) {
	if ( value.length < 6 )
	{
		return '请输入大于六位的密码' ;
	}
	else
	{
		if($("[name=password1_again]").length>0)
		{
			return $("[name=password1_again]").attr('value') == $("[name=password_1nd]").attr('value') ? true : '两次密码必须相等' ;
		}
		else
		{
			return true ;
		}
	}
});


$.tools.validator.fn("[name=password_2nd],[name=password2_again]", {"cn":'$1'} , function (input, value) {
	if ( value.length < 6 )
	{
		return '请输入大于六位的密码' ;
	}
	else
	{
		if($("[name=password2_again]").length>0)
		{
			return $("[name=password_2nd]").attr('value') == $("[name=password2_again]").attr('value') ? true : '两次密码必须相等' ;
		}
		else
		{
			return true ;
		}
	}
});


$.tools.validator.fn("[name=zip_code]", {"cn":'$1'} , function (input, value) {
	if ( value.length > 0 )
	{
		return /\d{6}$/.test(value) ? true : '请输入正确的邮政编码' ;
	}
	else
		return '请输入邮政编码' ;
});

$.tools.validator.fn("[name=street]", {"cn":'请输入街道名称'} , function (input, value) {
	return value.length > 0 ;
});

$.tools.validator.fn("[name=bank_account_id]", {"cn":'请输入正确的银行卡号'} , function (input, value) {
	return /[0-9]{19}/.test(value) > 0 ;
});

$.tools.validator.fn("[name=id_card_number],[name=id_card_num]", {"cn":'请输入正确的身份证号'} , function (input, value) {
	return /^[1-9]\d{5}[12]\d{3}[10]\d[0123]\d{4}[1-9Xx]$/.test(value) ;
});

$.tools.validator.fn("[name=name],[name=contact_name]", {"cn":'请输入中文。'} , function (input, value)
{
	return /^[\u4e00-\u9fa5]+$/.test(value) ;
});

