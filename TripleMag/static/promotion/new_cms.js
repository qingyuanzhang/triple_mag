var hasRequestDOM=false;var lastClickAnchorPoint="";jQuery(document).ready(function(){jumpUrl();initCmsImageLoad("cms_first_dom");if(hasNavigationMould){init_cms_navigation()}var a=location.href;if(a.indexOf("#")>-1){lastClickAnchorPoint=a.substr(a.indexOf("#"))}requestDom();cmsControlStock("cms_first_dom");if(jQuery.browser.msie&&(jQuery.browser.version=="6.0")&&!jQuery.support.style){jQuery.getScript(URLPrefix.statics+"/../js/v2/cms/DD_belatedPNG_0.0.8a-min.js",function(){DD_belatedPNG.fix(".skin_4_prize,.skin_4_3_list li,.skin_4_4_list li,.skin_4_5_list li,.skin_4_6_list li,div label,dl label,li label,.two_cols li,.three_cols li,.four_cols li,.five_cols li,.six_img,.six_cols,.skin_1_h2 a,.skin_1_h2,.buy_160a,.buy_160b,.buy_100a,.buy_100b,.img160 label,.red_box,.pink_box,.orange_box,.gold_box,.brown_box,.coffee_box,.green_box,.blue_box,.purple_box,.box_btm,.rt,.rm img,.lb,.lt,.lm,.lb,.middle_t,.middle_b")
})}});function jumpUrl(){var c=window.location.href;var d=c.substr(c.search("merchant=")+9,1);var a=c.split("&")[0];cookieProvinceId=jQuery.cookie("provinceId");var b="/cmsPage/getDefaultMerchantByProvinceId.do?provinceId="+cookieProvinceId+"&merchant="+d+"&rd="+Math.random();jQuery.getJSON(b,function(f){if(f.ERROR){}else{if(f.data.merId!=d){var e=a+"&merchant="+f.data.merId;gotoUrl(e)}}})}function gotoUrl(a){window.location.href=a}function cmsControlStock(g){var f=jQuery("#"+g);var a=[];var c=[];var e=[];var b=[];jQuery("a[lazyStore='y'][dataType='1']",f).each(function(h){c.push(jQuery(this).attr("productId"))});if(c.length>0){busystockLazy(c)}jQuery("a[lazyStore='y'][dataType='2']",f).each(function(h){a.push(jQuery(this).attr("langdingId"));e.push(jQuery(this).attr("productId"))});if(a.length>0){for(var d=a.length-1;
d>=1;d--){if(a[d-1]==a[d]){a.splice(d,1)}}landingpagestockLazy(a,e)}jQuery("a[lazyStore='y'][dataType='3']",f).each(function(h){b.push(jQuery(this).attr("productId"))});if(b.length>0){promotionstockLazy(b)}}function busystockLazy(b){var d="";for(var c=0;c<b.length;c++){d+="&productIds="+b[c]}var e=jQuery.cookie("provinceId");if(d!=""){var a="http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite="+currSiteId+"&provinceId="+e+d+"&callback=?";jQuery.getJSON(a,function(h){if(h.ERROR){}else{for(var f=0;f<h.length;f++){var g=h[f];if(g==null){continue}if(g.productId==null){continue}if(g.productStock==-1){continue}if(g.defaultMerchantId==-1){continue}if(g.productPrice==-1){continue}if(g.productType==1){continue}if(g.productStock>0){jQuery("a[productId='"+g.productId+"'][dataType='1']").each(function(j){jQuery(this).attr("href",jQuery(this).attr("tf"))
})}else{jQuery("a[productId='"+g.productId+"'][dataType='1']").each(function(j){jQuery(this).attr("href","###");jQuery(this).addClass("finished");jQuery(this).removeAttr("target");var k=jQuery(this).parents("*[name='"+g.defaultMerchantId+"_"+g.productId+"_1']").parent();jQuery("*[name='"+g.defaultMerchantId+"_"+g.productId+"_1']",k).appendTo(k)})}lazyLoadBusyStockPrice(g,1)}}})}}function landingpagestockLazy(a,d){var e="";for(var c=0;c<a.length;c++){e+="&promotionIds="+a[c]}var f=jQuery.cookie("provinceId");if(e!=""){var b="http://www.yihaodian.com/dynamicstock/getLandingPageStockAjax.do?provinceId="+f+e+"&callback=?";jQuery.getJSON(b,function(l){if(l.ERROR){}else{var g=l.value;if(g&&g.length>0){for(var h=0;h<g.length;h++){var k=g[h];if(k==null){continue}if(k.productId==null){continue}if(k.merchantId==-1){continue
}if(k.stockNum>0){jQuery("a[productId='"+k.productId+"'][dataType='2'][merchantId='"+k.merchantId+"']").each(function(m){jQuery(this).attr("href",jQuery(this).attr("tf"))})}else{jQuery("a[productId='"+k.productId+"'][dataType='2'][merchantId='"+k.merchantId+"']").each(function(m){jQuery(this).attr("href","###");jQuery(this).addClass("finished");jQuery(this).removeAttr("target");var n=jQuery(this).parents("*[name='"+k.merchantId+"_"+k.productId+"_2']").parent();jQuery("*[name='"+k.merchantId+"_"+k.productId+"_2']",n).appendTo(n)})}}}else{for(var h=0;h<d.length;h++){var j=d[h];jQuery("a[productId='"+j+"'][dataType='2']").each(function(m){jQuery(this).attr("href","###");jQuery(this).addClass("finished");jQuery(this).removeAttr("target")})}}}})}}function promotionstockLazy(a){var e="";for(var c=0;
c<a.length;c++){e+="&productIds="+a[c]}if(e!=""){var b="http://www.yihaodian.com/dynamicstock/getPromotionStockAjax.do?"+e+"&callback=?";jQuery.getJSON(b,function(k){if(k.ERROR){}else{var g=k.value;if(g&&g.length>0){for(var h=0;h<g.length;h++){var j=g[h];if(j==null){continue}if(j.productId==null){continue}if(j.merchantId==-1){continue}if(j.productPromPrice==-1){continue}if(j.stockNum>0){jQuery("a[productId='"+j.productId+"'][dataType='3'][merchantId='"+j.merchantId+"']").each(function(l){jQuery(this).attr("href",jQuery(this).attr("tf"))})}else{jQuery("a[productId='"+j.productId+"'][dataType='3'][merchantId='"+j.merchantId+"']").each(function(l){jQuery(this).attr("href","###");jQuery(this).addClass("finished");jQuery(this).removeAttr("target");var m=jQuery(this).parents("*[name='"+j.merchantId+"_"+j.productId+"_3']").parent();
jQuery("*[name='"+j.merchantId+"_"+j.productId+"_3']",m).appendTo(m)})}}}else{for(var h=0;h<a.length;h++){jQuery("a[productId='"+a[h]+"'][dataType='3']").each(function(l){jQuery(this).attr("href","###");jQuery(this).addClass("finished");jQuery(this).removeAttr("target")})}}}});var f=jQuery.cookie("provinceId");var d="http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite="+currSiteId+"&provinceId="+f+e+"&callback=?";jQuery.getJSON(d,function(j){if(j.ERROR){}else{for(var g=0;g<j.length;g++){var h=j[g];if(h==null){continue}if(h.productId==null){continue}if(h.productStock==-1){continue}if(h.defaultMerchantId==-1){continue}if(h.productPrice==-1){continue}if(h.productType==1){continue}lazyLoadBusyStockPrice(h,3)}}})}}function lazyLoadBusyStockPrice(b,a){jQuery("*[name='"+b.defaultMerchantId+"_"+b.productId+"_"+a+"']").each(function(c){var d=jQuery(".cms_product_price",this);
var f=jQuery(".cms_save",this);var e=jQuery(".cms_discount",this);if(d.length>0){d.html(b.productPrice)}if(f.length>0){f.html(returnFloat1(b.marketPrice-b.productPrice))}if(e.length>0){e.html(returnFloat1(b.productPrice*10/b.marketPrice)+"折")}})}function init_cms_navigation(){if(jQuery("div.rm img").length>0){jQuery("div.rm img").load(function(){var a=(jQuery(window).height()-jQuery("div.rm").outerHeight(true))/2;if(a<143){a=143}jQuery("div.rm").css("top",a).show()});jQuery("div.rm img").attr("src",jQuery("div.rm img").attr("navigationPic"))}if(jQuery("div.lm img").length>0){jQuery("div.lm img").load(function(){var a=(jQuery(window).height()-jQuery("div.lm").outerHeight(true))/2;if(a<143){a=143}jQuery("div.lm").css("top",a).show()});jQuery("div.lm img").attr("src",jQuery("div.lm img").attr("navigationPic"))
}if(jQuery("div.middle_b img").length>0){jQuery("div.middle_b img").load(function(){jQuery("body").css({paddingBottom:jQuery("div.middle_b").outerHeight(true)+"px"});jQuery("div.middle_b").show(0)});jQuery("div.middle_b img").attr("src",jQuery("div.middle_b img").attr("navigationPic"))}if(jQuery("div.middle_t img").length>0){jQuery("div.middle_t img").load(function(){jQuery("body").css({paddingTop:jQuery("div.middle_t").outerHeight(true)+"px"});jQuery("div.middle_t").show(0)});jQuery("div.middle_t img").attr("src",jQuery("div.middle_t img").attr("navigationPic"))}if(jQuery("div.rt img").length>0){jQuery("div.rt img").attr("src",jQuery("div.rt img").attr("navigationPic"))}if(jQuery("div.rb img").length>0){jQuery("div.rb img").attr("src",jQuery("div.rb img").attr("navigationPic"))}if(jQuery("div.lt img").length>0){jQuery("div.lt img").attr("src",jQuery("div.lt img").attr("navigationPic"))
}if(jQuery("div.lb img").length>0){jQuery("div.lb img").attr("src",jQuery("div.lb img").attr("navigationPic"))}jQuery(window).scroll(function(){if(jQuery.browser.msie&&(jQuery.browser.version=="6.0")&&!jQuery.support.style){var a=jQuery(window).scrollTop()+jQuery(window).height()-jQuery("div.middle_b").height();jQuery("div.lm").css({bottom:"auto",top:jQuery(window).scrollTop()+jQuery(window).height()/2-jQuery("div.lm").outerHeight(true)/2});jQuery("div.rm").css({bottom:"auto",top:jQuery(window).scrollTop()+jQuery(window).height()/2-jQuery("div.rm").outerHeight(true)/2});jQuery("div.lt,div.rt").css("top",jQuery(window).scrollTop()+"px");jQuery("div.middle_b").css({top:a});jQuery(".middle_t").css({top:jQuery(window).scrollTop()});jQuery("div.lb").css({bottom:"auto",top:jQuery(this).height()+jQuery(this).scrollTop()-jQuery("div.lb").outerHeight(true)}).show();
jQuery("div.rb").css({bottom:"auto",top:jQuery(this).height()+jQuery(this).scrollTop()-jQuery("div.rb").outerHeight(true)}).show()}}).trigger("scroll")}function requestDom(){if(!hasRequestDOM){hasRequestDOM=true;if(jQuery("#cms_second_dom").length>0){var b=jQuery("#cms_second_dom");var d=b.attr("lazyLoadMouldIDs");var a=b.attr("pageId");var c=b.attr("merchant");jQuery.get("/cmsPage/show.do",{pageId:a,merchant:c,lasyLoadDOM:true,lazyLoadMouldIDs:d},function(e){b.html(e);initCmsImageLoad("cms_second_dom");if(lastClickAnchorPoint!=""){window.location.hash=lastClickAnchorPoint}cmsControlStock("cms_second_dom")})}}}function initCmsImageLoad(a){lazyLoadImageObjArry=lazyLoadImageObjArry||[];jQuery("div[lazyImg='y']",jQuery("#"+a)).each(function(b){lazyLoadImageObjArry.push(this.id)});initImageLoad();
jQuery.YHD.imgLoad.load()}function gotoAnchorPiont(a){var b=jQuery(a).attr("href");if(b!=null&&b.substring(0,1)=="#"){if(jQuery(b).length<=0){lastClickAnchorPoint=b;requestDom()}}return true}function returnFloat1(a){a=Math.round(parseFloat(a)*10)/10;return a};