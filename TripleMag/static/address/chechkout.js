var YHDPlaceSelector = {
    init: function() {
        var a = '<select id="province" name="province"><option value="0">请选择省</option></select>';
        a += '<select id="city"  name="city"><option value="0">请选择市/区</option></select>';
        a += '<select id="county" name="county"><option value="0">请选择区/县</option></select>';
        a += '<select id="area" name="area"><option value="0">请选择四级区域</option></select>';
        a += '&nbsp;&nbsp;<a href="javascript:void(0);" onclick="popQueryWindow();">邮编查询所在地区</a>';
        a += '<label id="areaMessage" class="range red"></label>';
        jQuery("#placeSelector").html(a);
        jQuery("#city,#county,#area").hide();
        jQuery("#province").change(function() {
            var b = jQuery(this);
            var c = b.val();
            jQuery("#county,#area,#cityTip,#countyTip,#areaTip").empty().hide();
            jQuery("#postCode").val("");
            if (c == 0) {
                jQuery("#provinceTip,#city").empty().hide()
            } else {
                YHDPlaceSelector.refresh("#city", 2, c);
                jQuery("#provinceTip").html(b.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        });
        jQuery("#city").change(function() {
            var b = jQuery(this);
            var c = b.val();
            jQuery("#area,#countyTip,#areaTip").empty().hide();
            jQuery("#postCode").val("");
            if (c == 0) {
                jQuery("#cityTip,#county").empty().hide()
            } else {
                YHDPlaceSelector.refresh("#county", 3, c);
                jQuery("#cityTip").html(b.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        });
        jQuery("#county").change(function() {
            var c = jQuery(this);
            var d = c.val();
            jQuery("#areaTip").empty().hide();
            var b = c.find(":selected").attr("postcode");
            if (b == null || b == "null" || b == undefined) {
                b = ""
            }
            jQuery("#postCode").val(b);
            if (d == 0) {
                jQuery("#countyTip,#area").empty().hide()
            } else {
                YHDPlaceSelector.refresh("#area", 4, d);
                jQuery("#countyTip").html(c.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        });
        jQuery("#area").change(function() {
            var c = jQuery(this);
            var e = c.val();
            var d = jQuery("#county").find(":selected").attr("postcode");
            var b = c.find(":selected").attr("postcode");
            if (d == null || d == "null" || d == undefined) {
                d = ""
            }
            if (b == null || b == "null" || b == undefined) {
                b = ""
            }
            if (e == 0) {
                jQuery("#postCode").val(d);
                jQuery("#areaTip").empty().hide()
            } else {
                jQuery("#postCode").val(b);
                jQuery("#areaTip").html(c.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        })
    },
    refresh: function(f, b, e, c) {
        if ((c == 0) && b == 4) {
            jQuery(f).empty().hide();
            return
        } else {
            var a = "/checkout/address/ajaxGetPlaceList.do";
            var d = {
                id: e,
                type: b
            };
            jQuery.post(a, d,
            function(g) {
                if (g.message == "success" && g.data != null && g.data.length > 0) {
                    YHDPlaceSelector.showUI(f, b, e, c, g.data)
                }
            },
            "json")
        }
    },
    showUI: function(g, a, f, b, c) {
        var d = "请选择";
        if (a == 1) {
            d = "请选择省"
        } else {
            if (a == 2) {
                d = "请选择市/区"
            } else {
                if (a == 3) {
                    d = "请选择区/县"
                } else {
                    if (a == 4) {
                        d = "请选择四级区域"
                    }
                }
            }
        }
        if ((b == 0) && a == 4 && map_load != 2) {
            jQuery(g).empty().hide();
            jQuery(g + "Tip").hide();
            return
        } else {
            if (c != null && c.length > 0) {
                jQuery(g).empty();
                var h = '<option value="0">' + d + "</option>";
                var e = 0;
                jQuery(c).each(function(i) {
                    if (i == 0) {
                        e = this.id
                    }
                    if (f == this.id && a == 4) {} else {
                        if (this.id == b) {
                            h += '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                        } else {
                            if (a == 4 && c.length == 1 && jQuery("#county").find(":selected").text() == this.name) {
                                h = '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                            } else {
                                h += '<option value="' + this.id + '" postcode="' + this.postcode + '">' + this.name + "</option>"
                            }
                        }
                    }
                });
                jQuery(g).html(h);
                if (b != null) {
                    if ((f == b) && a == 4) {} else {
                        jQuery(g).attr("value", b)
                    }
                    if (b != 0) {
                        if ((f == b) && a == 4) {
                            jQuery(g + "Tip").hide()
                        } else {
                            jQuery(g + "Tip").html(jQuery(g).find(":selected").text() + "&nbsp;&nbsp;").show()
                        }
                    }
                }
                if (f == e && c.length == 1 && a == 4) {
                    jQuery(g).empty().hide();
                    jQuery(g + "Tip").hide()
                } else {
                    if (c.length == 1 && a == 4 && jQuery("#county").find(":selected").text() == c[0].name) {
                        jQuery(g).hide()
                    } else {
                        jQuery(g).show()
                    }
                }
            } else {
                jQuery(g).empty().hide()
            }
        }
    },
    updateDefaultCheckedStatus: function(c, d, e, b) {
        var f = "/checkout/address/ajaxGetFourPlaceLists.do";
        var a = {
            provinceId: c,
            cityId: d,
            countyId: e
        };
        jQuery.post(f, a,
        function(i) {
            if (i && i.message == "success") {
                var k = i.data.provinceList;
                var g = i.data.cityList;
                var h = i.data.countyList;
                var j = i.data.areaList;
                if (c != null && c != 0) {
                    YHDPlaceSelector.showUI("#province", 1, 1, c, k);
                    YHDPlaceSelector.showUI("#city", 2, c, d, g);
                    YHDPlaceSelector.showUI("#county", 3, d, e, h);
                    YHDPlaceSelector.showUI("#area", 4, e, b, j)
                } else {
                    YHDPlaceSelector.showUI("#province", 1, 1, 0, k)
                }
            } else {
                alert("网络出现异常,请稍后重试!")
            }
        },
        "json")
    },
    initDefaultCheckedStatus: function() {
        YHDPlaceSelector.init();
        var a = jQuery("#placeSelector").attr("provinceId");
        var b = jQuery("#placeSelector").attr("cityId");
        var c = jQuery("#placeSelector").attr("countyId");
        var d = jQuery("#placeSelector").attr("areaId");
        YHDPlaceSelector.updateDefaultCheckedStatus(a, b, c, d)
    },
    clearDefaultCheckedStatus: function() {
        jQuery("#province").attr("value", 0);
        jQuery("#city,#county,#area").empty().hide();
        jQuery("#provinceTip,#cityTip,#countyTip,#areaTip").empty().hide()
    }
};
var manyFourPlace = 0;
var cityChange = 0;
var YHDMapPlaceSelector = {
    init: function() {
        var a = '<select id="province" name="province"><option value="0">请选择省</option></select>';
        a += '<select id="city"  name="city"><option value="0">请选择市/区</option></select>';
        a += '<select id="county" name="county"><option value="0">请选择区/县</option></select>';
        a += '<select id="area" name="area"></select>';
        jQuery("#placeSelector").html(a);
        jQuery("#city,#county,#area").hide();
        if (isBigCity()) {
            jQuery("#countyTip", "#areaTip").empty().hide()
        } else {
            jQuery("#areaTip").empty().hide()
        }
        jQuery("#province").change(function() {
            var b = jQuery(this);
            var c = b.val();
            jQuery("#county,#area,#cityTip,#countyTip,#areaTip").empty().hide();
            jQuery("#postCode").val("");
            if (c == 0) {
                jQuery("#provinceTip,#city").empty().hide()
            } else {
                YHDMapPlaceSelector.refresh("#city", 2, c);
                jQuery("#provinceTip").html(b.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        });
        jQuery("#city").change(function() {
            var b = jQuery(this);
            var c = b.val();
            jQuery("#area,#countyTip,#areaTip").empty().hide();
            jQuery("#postCode").val("");
            cityChange = 1;
            if (c == 0) {
                jQuery("#cityTip,#county").empty().hide()
            } else {
                YHDMapPlaceSelector.refresh("#county", 3, c);
                jQuery("#cityTip").html(b.find(":selected").text() + "&nbsp;&nbsp;").show();
                getCurrAddress();
                if (jQuery("#detailAddress").val() != "" || jQuery("#detailAddress").val() != null) {
                    areaAddress()
                }
            }
        });
        jQuery("#county").change(function() {
            var c = jQuery(this);
            var d = c.val();
            jQuery("#areaTip").empty().hide();
            var b = c.find(":selected").attr("postcode");
            if (b == null || b == "null" || b == undefined) {
                b = ""
            }
            jQuery("#postCode").val(b);
            if (d == 0) {
                jQuery("#countyTip,#area").empty().hide()
            } else {
                YHDMapPlaceSelector.refresh("#area", 4, d);
                jQuery("#countyTip").html(c.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
        })
    },
    refresh: function(f, b, e, c) {
        if ((c == 0) && b == 4) {
            jQuery(f).empty().hide();
            return
        } else {
            var a = "/checkout/address/ajaxGetPlaceList.do";
            var d = {
                id: e,
                type: b
            };
            jQuery.post(a, d,
            function(g) {
                if (g.message == "success" && g.data != null && g.data.length > 0) {
                    YHDMapPlaceSelector.showUI(f, b, e, c, g.data);
                    if (b == 4 && g.data.length > 1) {
                        manyFourPlace = 1
                    } else {
                        manyFourPlace = 0
                    }
                }
            },
            "json")
        }
    },
    showUI: function(g, a, f, b, c) {
        var d = "请选择";
        if (a == 1) {
            d = "请选择省"
        } else {
            if (a == 2) {
                d = "请选择市/区"
            } else {
                if (a == 3) {
                    d = "请选择区/县"
                } else {
                    if (a == 4) {
                        d = "请选择四级区域"
                    }
                }
            }
        }
        if ((b == 0) && a == 4) {
            jQuery(g).empty().hide();
            jQuery(g + "Tip").hide();
            return
        } else {
            if (c != null && c.length > 0) {
                if ((isBigCity() && a < 3) || (!isBigCity() && a < 4)) {
                    jQuery(g).empty();
                    var h = '<option value="0">' + d + "</option>";
                    var e = 0;
                    jQuery(c).each(function(i) {
                        if (i == 0) {
                            e = this.id
                        }
                        if (f == this.id && a == 4) {} else {
                            if (this.id == b) {
                                h += '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                            } else {
                                h += '<option value="' + this.id + '" postcode="' + this.postcode + '">' + this.name + "</option>"
                            }
                        }
                    });
                    jQuery(g).html(h);
                    if (b != null) {
                        if ((f == b) && a == 4) {} else {
                            jQuery(g).attr("value", b)
                        }
                        if (b != 0) {
                            if ((f == b) && a == 4) {
                                jQuery(g + "Tip").hide()
                            } else {
                                jQuery(g + "Tip").html(jQuery(g).find(":selected").text() + "&nbsp;&nbsp;").show()
                            }
                        }
                    }
                    if (f == e && c.length == 1 && a == 4) {
                        jQuery(g).empty().hide();
                        jQuery(g + "Tip").hide()
                    } else {
                        jQuery(g).show()
                    }
                } else {
                    if (g == "#county") {
                        var h = "";
                        jQuery(c).each(function(i) {
                            if (this.id == b) {
                                h = '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                            }
                        });
                        jQuery(g).html(h)
                    } else {
                        if (g == "#area") {
                            var h = "";
                            jQuery(c).each(function(i) {
                                if (this.id == b) {
                                    h = '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                                }
                            });
                            jQuery(g).html(h);
                            if ((f == b) && a == 4) {
                                jQuery(g + "Tip").hide()
                            } else {}
                        }
                    }
                }
            } else {
                jQuery(g).empty().hide()
            }
        }
    },
    updateDefaultCheckedStatus: function(c, d, e, b) {
        var f = "/checkout/address/ajaxGetFourPlaceLists.do";
        var a = {
            provinceId: c,
            cityId: d,
            countyId: e
        };
        jQuery.post(f, a,
        function(i) {
            if (i && i.message == "success") {
                var k = i.data.provinceList;
                var g = i.data.cityList;
                var h = i.data.countyList;
                var j = i.data.areaList;
                if (c != null && c != 0) {
                    YHDMapPlaceSelector.showUI("#province", 1, 1, c, k);
                    YHDMapPlaceSelector.showUI("#city", 2, c, d, g);
                    YHDMapPlaceSelector.showUI("#county", 3, d, e, h);
                    YHDMapPlaceSelector.showUI("#area", 4, e, b, j)
                } else {
                    YHDMapPlaceSelector.showUI("#province", 1, 1, 0, k)
                }
            } else {
                alert("网络出现异常,请稍后重试!")
            }
        },
        "json")
    },
    initDefaultCheckedStatus: function() {
        YHDMapPlaceSelector.init();
        var a = jQuery("#placeSelector").attr("provinceId");
        var b = jQuery("#placeSelector").attr("cityId");
        var c = jQuery("#placeSelector").attr("countyId");
        var d = jQuery("#placeSelector").attr("areaId");
        YHDMapPlaceSelector.updateDefaultCheckedStatus(a, b, c, d)
    },
    clearDefaultCheckedStatus: function() {
        jQuery("#province").attr("value", 0);
        jQuery("#city,#county,#area").empty().hide();
        jQuery("#provinceTip,#cityTip,#countyTip,#areaTip").empty().hide()
    }
};
function isBigCity() {
    var a = jQuery("#province").val();
    if (a == 1 || a == 2) {
        return true
    } else {
        return false
    }
}
var YHDPlaceSelectorWithoutProvice = {
    init: function() {
        var a = '<select id="city"  name="city"><option value="0">请选择市/区</option></select>';
        a += '<select id="county" name="county"><option value="0">请选择区/县</option></select>';
        a += '<select id="area" name="area"><option value="0">请选择四级区域</option></select>';
        a += '<label id="areaMessage" class="range red"></label>';
        jQuery("#detailPlaceSelector").html(a);
        jQuery("#city,#county,#area").hide();
        jQuery("#city").change(function() {
            var b = jQuery(this);
            var c = b.val();
            jQuery("#area,#countyTip,#areaTip").empty().hide();
            jQuery("#postCode").val("");
            if (c == 0) {
                jQuery("#cityTip,#county").empty().hide();
                jQuery("#deliveryStr").hide()
            } else {
                YHDPlaceSelectorWithoutProvice.refresh("#county", 3, c);
                jQuery("#cityTip").html(b.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
            changeDeliveryFeeLink()
        });
        jQuery("#county").change(function() {
            var c = jQuery(this);
            var d = c.val();
            jQuery("#areaTip").empty().hide();
            var b = c.find(":selected").attr("postcode");
            if (b == null || b == "null" || b == undefined) {
                b = ""
            }
            jQuery("#postCode").val(b);
            if (d == 0) {
                jQuery("#countyTip,#area").empty().hide();
                jQuery("#deliveryStr").hide()
            } else {
                jQuery("#deliveryStr").show();
                YHDPlaceSelectorWithoutProvice.refresh("#area", 4, d);
                jQuery("#countyTip").html(c.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
            changeDeliveryFeeLink();
            showMsgAfterChArea();
            saveCookie()
        });
        jQuery("#area").change(function() {
            var c = jQuery(this);
            var e = c.val();
            var d = jQuery("#county").find(":selected").attr("postcode");
            var b = c.find(":selected").attr("postcode");
            if (d == null || d == "null" || d == undefined) {
                d = ""
            }
            if (b == null || b == "null" || b == undefined) {
                b = ""
            }
            if (e == 0) {
                jQuery("#postCode").val(d);
                jQuery("#areaTip").empty().hide()
            } else {
                changeDeliveryFeeLink();
                jQuery("#deliveryStr").show();
                jQuery("#postCode").val(b);
                jQuery("#areaTip").html(c.find(":selected").text() + "&nbsp;&nbsp;").show()
            }
            showMsgAfterChArea();
            saveCookie()
        })
    },
    updateDefaultCheckedStatus: function(c, d, b) {
        var e = "/product/ajaxGetDetailPlaceList.do";
        var a = {
            cityId: c,
            countyId: d
        };
        jQuery.post(e, a,
        function(h) {
            if (h && h.message == "success") {
                var f = h.data.cityList;
                var g = h.data.countyList;
                var i = h.data.areaList;
                YHDPlaceSelectorWithoutProvice.showUI("#city", 2, 1, c, f);
                YHDPlaceSelectorWithoutProvice.showUI("#county", 3, c, d, g);
                YHDPlaceSelectorWithoutProvice.showUI("#area", 4, d, b, i)
            }
        },
        "json")
    },
    showUI: function(g, a, f, b, c) {
        var d = "请选择";
        if (a == 2) {
            d = "请选择市/区"
        } else {
            if (a == 3) {
                d = "请选择区/县"
            } else {
                if (a == 4) {
                    d = "请选择四级区域"
                }
            }
        }
        if ((b == 0) && a == 4) {
            jQuery(g).empty().hide();
            jQuery(g + "Tip").hide();
            return
        } else {
            if (c != null && c.length > 0) {
                jQuery(g).empty();
                var h = '<option value="0">' + d + "</option>";
                var e = 0;
                jQuery(c).each(function(i) {
                    if (i == 0) {
                        e = this.id
                    }
                    if (f == this.id && a == 4) {} else {
                        if (this.id == b) {
                            h += '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                        } else {
                            if (a == 4 && c.length == 1 && jQuery("#county").find(":selected").text() == this.name) {
                                h = '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>"
                            }
                            if (c.length == 1 && jQuery("#city").find(":selected").text() == this.name) {
                                h = '<option value="' + this.id + '" postcode="' + this.postcode + '" selected>' + this.name + "</option>";
                                setTimeout("showMsgAfterChArea()", 500);
                                setTimeout("showMsgAfterChArea()", 500);
                                saveCookie()
                            } else {
                                h += '<option value="' + this.id + '" postcode="' + this.postcode + '">' + this.name + "</option>"
                            }
                        }
                    }
                });
                jQuery(g).html(h);
                if (b != null) {
                    if ((f == b) && a == 4) {} else {
                        jQuery(g).attr("value", b)
                    }
                    if (b != 0) {
                        if ((f == b) && a == 4) {
                            jQuery(g + "Tip").hide()
                        } else {
                            jQuery(g + "Tip").html(jQuery(g).find(":selected").text() + "&nbsp;&nbsp;").show()
                        }
                    }
                }
                if (f == e && c.length == 1 && a == 4) {
                    jQuery(g).empty().hide();
                    jQuery(g + "Tip").hide()
                } else {
                    if (c.length == 1 && a == 4 && jQuery("#county").find(":selected").text() == c[0].name) {
                        jQuery(g).hide()
                    } else {
                        jQuery(g).show()
                    }
                }
            } else {
                jQuery(g).empty().hide()
            }
        }
    },
    initDefaultCheckedStatus: function() {
        YHDPlaceSelectorWithoutProvice.init();
        var b = jQuery("#detailPlaceSelector").attr("countyId");
        var c = jQuery("#detailPlaceSelector").attr("areaId");
        var a = jQuery("#detailPlaceSelector").attr("cityId");
        YHDPlaceSelectorWithoutProvice.updateDefaultCheckedStatus(a, b, c)
    },
    refresh: function(f, b, e, c) {
        if ((c == 0) && b == 4) {
            jQuery(f).empty().hide();
            return
        } else {
            var a = "/checkout/address/ajaxGetPlaceList.do";
            var d = {
                id: e,
                type: b
            };
            jQuery.post(a, d,
            function(g) {
                if (g.message == "success" && g.data != null && g.data.length > 0) {
                    YHDPlaceSelectorWithoutProvice.showUI(f, b, e, c, g.data);
                    if (b == 4 && g.data.length > 1) {
                        jQuery("#deliveryStr").hide();
                        manyFourPlace = 1
                    } else {
                        manyFourPlace = 0
                    }
                }
            },
            "json")
        }
    }
};
String.prototype.mylength = function() {
    var b = this.match(/[\u00FF-\uFFFF]/gi);
    if (!b || b == null) {
        return this.length
    }
    var a = this.length + b.length;
    return a
};
String.prototype.trim = function() {
    return this.replace(/(^\s*)|(\s*$)/g, "")
};
function formatToString(a) {
    if (a != null && a != "null" && a != undefined && a != "" && a.length > 0) {
        return a
    } else {
        return ""
    }
}
function len(e) {
    var c = 0;
    var b = e.split("");
    for (var d = 0; d < b.length; d++) {
        if (b[d].charCodeAt(0) < 299) {
            c++
        } else {
            c += 2
        }
    }
    return c
}
function showWaitInfo(d, c) {
    try {
        if (c == null) {
            return
        }
        clearWaitInfo();
        var b = document.createElement("span");
        b.className = "waitInfo";
        b.id = "waitInfo";
        b.innerHTML = d;
        c.parentNode.appendChild(b)
    } catch(a) {}
}
function showWaitInfoOnInner(d, c) {
    try {
        if (c == null) {
            return
        }
        clearWaitInfo();
        var b = document.createElement("span");
        b.className = "waitInfo";
        b.id = "waitInfo";
        b.innerHTML = d;
        c.innerHTML = "";
        c.appendChild(b)
    } catch(a) {}
}
function clearWaitInfo() {
    try {
        if (jQuery("#waitInfo") != null) {
            jQuery("#waitInfo").remove()
        }
    } catch(a) {}
}
function hasErrors() {
    var a = jQuery("#errorMsgDisplayDiv").html();
    return a && a.trim().length > 10
}
function doShowErrors() {
    if (hasErrors()) {
        YHD.alert(jQuery("#errorMsgDisplayDiv").html(), returnCart)
    }
    jQuery("#errorMsgDisplayDiv").hide()
}
function showCheckoutAjaxErrorPopwin() {
    if (jQuery("#checkoutAjaxErrorDiv").size() > 0) {
        YHD.popwin(jQuery("#checkoutAjaxErrorDiv").html(), null, null, "200px", "400px");
        jQuery(window).scroll(function() {
            jQuery("#yhd_pop_win").css({
                top: jQuery(document).scrollTop() + jQuery(window).height() - jQuery("#yhd_pop_win").height() - 500
            })
        })
    }
}
function redirectIfNotLogin(d) {
    if (d) {
        var f = "/passport/login.do";
        var e = "password";
        if (d.indexOf(f) != -1 && d.indexOf(e) != -1) {
            window.location.href = "/passport/login_input.do";
            return false
        }
        var c = "URL=/not_found.do";
        if (d.indexOf(c) != -1) {
            window.location.href = "/not_found.do";
            return false
        }
        var a = "errorPageFlag";
        if (d.indexOf(a) != -1) {
            window.location.href = "/product/cart.do?action=view";
            return false
        }
        var b = "checkoutAjaxErrorFlg";
        if (d.indexOf(b) != -1) {
            showCheckoutAjaxErrorPopwin();
            return false
        }
    }
    return true
}
function Round(i, digit) {
    if (isNaN(parseFloat(i))) {
        return "0"
    }
    if (digit == 0) {
        p = 1
    } else {
        if (digit) {
            p = Math.pow(10, digit)
        } else {
            p = 100
        }
    }
    var mm = Math.round(i * p) / p;
    var strTmp = eval("'" + mm + "'");
    var behind = "";
    if (strTmp.indexOf(".") >= 0) {
        behind = strTmp.substring(strTmp.indexOf(".") + 1, strTmp.length);
        while (digit - behind.length > 0) {
            behind += "0"
        }
        strTmp = strTmp.substring(0, strTmp.indexOf(".") + 1) + behind
    } else {
        for (var j = 0; j < digit; j++) {
            behind += "0"
        }
        if (digit > 0) {
            strTmp = strTmp + "." + behind
        }
    }
    return strTmp
};
var updated = false;
var create = false;
var ids = new Array();
var index = 0;
var updateReceiver = false;
var updateDelivery = false;
var updatePayment = false;
var submitBtnDisplay = false;
var paymentSpecControl = false;
var invoceControl = false;
var isValidCodeNeed = 0;
function controlSwitchWindow(a) {
    if (a == 1) {
        jQuery("#head_info_check").css("display", "none");
        doModifyAddress();
        jQuery("#receiver_buffer_window").show();
        jQuery("#delivery_buffer_window").hide();
        jQuery("#payment_buffer_window").hide();
        jQuery("#goods_buffer_window").hide()
    }
    if (a == 2) {
        jQuery("#head_info_check").css("display", "block");
        jQuery("#receiver_info_check").css("display", "block");
        jQuery("#delivery_info_check").css("display", "none");
        jQuery("#payment_info_check").css("display", "none");
        doModifyDelivery();
        jQuery("#receiver_buffer_window").hide();
        jQuery("#delivery_buffer_window").show();
        jQuery("#payment_buffer_window").hide();
        jQuery("#goods_buffer_window").hide()
    }
    if (a == 3) {
        jQuery("#head_info_check").css("display", "block");
        jQuery("#receiver_info_check").css("display", "block");
        jQuery("#delivery_info_check").css("display", "block");
        jQuery("#payment_info_check").css("display", "none");
        doModifyPayment();
        jQuery("#receiver_buffer_window").hide();
        jQuery("#delivery_buffer_window").hide();
        jQuery("#payment_buffer_window").show();
        jQuery("#goods_buffer_window").hide()
    }
    if (a == 4) {
        jQuery("#head_info_check").css("display", "block");
        jQuery("#receiver_info_check").css("display", "block");
        jQuery("#delivery_info_check").css("display", "block");
        jQuery("#payment_info_check").css("display", "block");
        doGetAmountList();
        getWLTPoints();
        jQuery("#receiver_buffer_window").hide();
        jQuery("#delivery_buffer_window").hide();
        jQuery("#payment_buffer_window").hide();
        jQuery("#goods_buffer_window").show()
    }
}
function addID(a) {
    ids[index++] = a
}
function checkSubmitBtnDisplay() {}
function controlSubmitBtnDisplay() {
    if (submitBtnDisplay) {
        jQuery("#submitbtn").css("display", "")
    } else {
        jQuery("#submitbtn").css("display", "none")
    }
}
function returnCart() {
    flow_step = 1;
    renderUI();
    return false
}
function updateFlowBar(b) {
    if (b == -1) {
        b = 4
    }
    var a = "fl step" + b;
    jQuery("#flowBar").removeClass();
    jQuery("#flowBar").addClass(a)
}
function renderUI() {
    updateFlowBar(flow_step);
    controlSwitchWindow(flow_step);
    jQuery("div.row:gt(4)").hide();
    myAddressHover()
}
function initUI() {
    renderUI()
}
function isValiCodeNeed() {
    var a = "/checkout/confirm/isValiCodeNeed.do";
    var b = {
        rd: Math.random()
    };
    jQuery.get(a, b,
    function(c) {
        isValidCodeNeed = c.data;
        if (c.data >= 1) {
            jQuery("#validCodeCheck").css("display", "block")
        } else {
            jQuery("#validCodeCheck").css("display", "none")
        }
    })
}
function toggleAddressModel() {
    var c = jQuery("#province").val();
    var b = jQuery("#city").val();
    var a = jQuery("#county").val();
    jQuery("#placeSelector").attr("provinceId", c);
    jQuery("#placeSelector").attr("cityId", b);
    if (a == null || a == "") {
        jQuery("#placeSelector").attr("countyId", 0)
    } else {
        jQuery("#placeSelector").attr("countyId", a)
    }
    jQuery("#placeSelector").attr("areaId", 0);
    if (map_load == 1) {
        YHDPlaceSelector.initDefaultCheckedStatus();
        map_load = 2
    } else {
        YHDMapPlaceSelector.initDefaultCheckedStatus();
        map_load = 1
    }
}
jQuery(document).ready(function() {
    doShowErrors();
    initUI();
    if (flow_step == 1) {
        if (map_load == 1) {
            YHDMapPlaceSelector.initDefaultCheckedStatus()
        } else {
            YHDPlaceSelector.initDefaultCheckedStatus()
        }
    }
    jQuery(".cont").hide()
});
var attached = false;
function submitAttachedObjectInfo() {
    if (!checkAttachedForm()) {
        return false
    }
    var b = "/product/updateAtttachedInfo.do";
    var a = $("attachedFrm").serialize();
    jQuery.post(b, a, updateAttachedFlag)
}
function updateAttachedFlag(a) {
    redirectIfNotLogin(a);
    attached = true;
    $("attachedObjectSelect").innerHTML = a.responseText;
    $("attachedObjectList").hide();
    $("modifyAttachedLink").show();
    $("attachedObjectSelect").show()
}
function checkAttachedForm() {
    var n = true;
    var d = $("attachedFrm");
    if (!d) {
        attached = true
    } else {
        var e = document.getElementsByName("mandatory_prop");
        if (e.length > 0) {
            for (var g = 0; g < e.length; g++) {
                var m = true;
                var b = e[g].value;
                var d = document.getElementsByName(b);
                var h;
                for (var f = 0; f < d.length; f++) {
                    var l = d[f];
                    h = d[0];
                    var k = l.type;
                    if (k == "radio" || k == "checkbox") {
                        if (l.checked) {
                            m = false;
                            break
                        }
                    }
                    if (k == "text" || k == "textarea") {
                        if (b.indexOf("pingan:cardnum") != -1) {
                            if (l.value) {
                                var a = /^E([0-9]){10}$/;
                                var o = /^[A-Z0-9]{16,20}$/;
                                if (!a.exec(l.value) && !o.exec(l.value)) {
                                    alert("请输入正确的平安集团员工代码或者客户保单号码");
                                    h.focus();
                                    return false
                                }
                            }
                        }
                        if (l.value != "" && l.value.trim() != "") {
                            m = false;
                            break
                        }
                    }
                }
                if (m) {
                    h.focus();
                    alert("请填写附加信息");
                    n = false;
                    break
                }
            }
        }
    }
    return n
}
function refreshValidCode() {
    var a = new Date();
    jQuery("#validCodePic").attr("src", "/checkout/confirm/GenValidCode.do?t=" + a)
}
function submitValidCode() {
    var c = jQuery("#validPicValue").val();
    var a = "/checkout/confirm/ConfirmValidCode.do";
    var b = {
        rd: Math.random(),
        validCodeValueOfPage: c
    };
    jQuery.get(a, b,
    function(d) {
        if (d.data == null) {
            d.data = 0
        }
        if (d.data == 1) {
            jQuery("#validError").hide();
            doSaveInvoice()
        } else {
            jQuery("#validError").show()
        }
    })
}
function submitOrder() {
    placeOrder(this);
    gotracker("2", "placeOrderButton", null)
}
function onTypeCode() {
    jQuery("#validError").hide()
};
function doModifyDelivery(a) {
    if (a) {
        showWaitInfo("正在读取送货方式，请等待。。。", a)
    }
    updateDelivery = true;
    controlSubmitBtnDisplay();
    changeDeliveryType( - 1)
}
function changeDeliveryType(c) {
    var b = jQuery("#county").val();
    var a = "deliveryType=" + c;
    if (b) {
        if (b == 0) {
            b = jQuery("#default_county_id").val()
        }
        a += "&county.id=" + b
    }
    jQuery.post("/checkout/ship/index.do?rd=" + Math.random(), a, updateDeliveryMethod)
}
function updateDeliveryMethod(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    } else {
        jQuery("#delivery_buffer_window").html(a);
        jQuery("#deliveryListDiv").css("display", "block");
        clearWaitInfo();
        initDeliveryMethodSelectorEvent()
    }
}
function doSaveDelivery(b) {
    var a = "/checkout/ship/confirmSaveOrderDeliveryMethod.do?rd=" + Math.random();
    var c = getDeliveryPostParams();
    jQuery.post(a, c,
    function(d) {
        afterSaveDelivery(d)
    })
}
function afterSaveDelivery(a) {
    jQuery("#confirm_delivery").removeAttr("disabled");
    if (a.indexOf("DATE_ERROR") >= 0) {
        YHD.alert("很抱歉，您选择的期望收货日期不正确。");
        return false
    }
    if (!redirectIfNotLogin(a)) {
        return false
    } else {
        jQuery("#deliveryListDiv").css("display", "none");
        jQuery("#deliveryInfoDiv").html(a);
        clearWaitInfo();
        flow_step = 3;
        renderUI()
    }
}
function refreshShipPage(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    } else {
        jQuery("#delivery_buffer_window").html(a);
        jQuery("#deliveryListDiv").css("display", "block");
        initDeliveryMethodSelectorEvent()
    }
}
function unitOrderShip() {
    var a = "/checkout/ship/unitOrderShip.do?rd=" + Math.random();
    var b = getSendOrderMarkParams(1);
    jQuery.get(a, b,
    function(c) {
        refreshShipPage(c)
    })
}
function splitOrderShip() {
    var a = "/checkout/ship/splitOrderShip.do?rd=" + Math.random();
    var b = getSendOrderMarkParams(2);
    jQuery.get(a, b,
    function(c) {
        refreshShipPage(c)
    })
}
function initDeliveryMethodSelectorEvent() {
    jQuery("select.deliveryMethodSelector").change(function() {
        var a = jQuery(this).val();
        var b = jQuery(this).attr("orderMark");
        if (a == 10002) {
            jQuery("#assignDate" + b).show();
            jQuery("#halfDay" + b).hide();
            jQuery("#oneDayThree" + b).hide();
            refreshOrderDeliveryFee()
        } else {
            if (a == 10004) {
                jQuery("#assignDate" + b).hide();
                jQuery("#halfDay" + b).show();
                jQuery("#oneDayThree" + b).hide();
                if (jQuery("input.halfdayTimeRadio" + b + ":radio:checked").size() == 0) {
                    jQuery("input.halfdayTimeRadio" + b + ":radio").eq(0).attr("checked", true);
                    refreshOrderDeliveryFee()
                } else {
                    refreshOrderDeliveryFee()
                }
            } else {
                if (a == 10003) {
                    jQuery("#assignDate" + b).hide();
                    jQuery("#halfDay" + b).hide();
                    jQuery("#oneDayThree" + b).show();
                    if (jQuery("input.oneDayThreeTimeRadio" + b + ":radio:checked").size() == 0) {
                        jQuery("input.oneDayThreeTimeRadio" + b + ":radio").eq(0).attr("checked", true);
                        refreshOrderDeliveryFee()
                    } else {
                        refreshOrderDeliveryFee()
                    }
                } else {
                    jQuery("#assignDate" + b).hide();
                    jQuery("#halfDay" + b).hide();
                    jQuery("#oneDayThree" + b).hide();
                    refreshOrderDeliveryFee()
                }
            }
        }
    });
    jQuery("input[name=datePickerInput]").click(function() {
        var a = jQuery(this);
        showDatePicker(a)
    });
    jQuery("input.deliveryTimeRadio:radio").unbind();
    jQuery("input.deliveryTimeRadio:radio").click(function() {
        refreshOrderDeliveryFee()
    })
}
function showDatePicker(d) {
    var a = jQuery(d).attr("startDate");
    var b = jQuery(d).attr("disabledDate");
    var c = jQuery(d).attr("endDate");
    jQuery(d).datePicker().dpSetDisabledDate(b).dpSetStartDate(a).dpSetEndDate(c)
}
function refreshOrderDeliveryFee() {
    var a = "/checkout/ship/ajaxRefreshOrderDeliveryFee.do?rd=" + Math.random();
    var b = getDeliveryPostParams();
    jQuery("#doSaveDeliveryBtn").attr("disabled", true);
    jQuery.post(a, b,
    function(d) {
        jQuery("#doSaveDeliveryBtn").attr("disabled", false);
        if (d && d.message == "success") {
            var f = d.data.totalYihaodianDeliveryFee;
            var e = d.data.totalYihaodianAmount;
            var c = d.data.almostGiftFlag;
            refreshAlmostGiftFlag(c);
            jQuery("#totalYihaodianDeliveryFee").text(f);
            jQuery("#totalYihaodianAmount").text(e)
        } else {
            showCheckoutAjaxErrorPopwin();
            return false
        }
    },
    "json")
}
function refreshAlmostGiftFlag(a) {
    var b = a - 1;
    if (b < 0) {
        b = 0
    }
    jQuery(".almostOrder").hide();
    jQuery(".almostOrder").eq(b).show()
}
function getSendOrderMarkParams(b) {
    var a = "";
    jQuery("input.sendOrderRadio:radio:checked").each(function() {
        var c = jQuery(this).val();
        if (c == b) {
            var d = jQuery(this).attr("orderMark");
            a += "&orderMarks=" + d
        }
    });
    if (a.length > 0) {
        a = a.substring(1)
    }
    return a
}
function getDeliveryPostParams() {
    var a = "";
    jQuery("select.deliveryMethodSelector").each(function() {
        var f = jQuery(this).attr("orderMark");
        var b = jQuery(this).val();
        b = parseInt(b);
        var d = "";
        var e = "";
        var c = "";
        if (b == 10002) {
            d = jQuery("#assignDate_datePickerInput" + f).val()
        } else {
            if (b == 10003) {
                d = jQuery("#oneDayThree_datePickerInput" + f).val();
                e = jQuery("[name=time" + f + "]:radio:checked").val()
            } else {
                if (b == 10004) {
                    d = jQuery("#halfday_datePickerInput" + f).val();
                    e = jQuery("[name=time" + f + "]:radio:checked").val()
                }
            }
        }
        if (jQuery("#receive_remarks" + f).size() > 0) {
            c = jQuery("#receive_remarks" + f).val()
        }
        a += "&orderMarks=" + f + "&selectedDeliveryMethodIds=" + b + "&receiverDates=" + d + "&selectedThreeOneDays=" + e + "&receive_remarks=" + c
    });
    if (a.length > 0) {
        a = a.substring(1)
    }
    return a
};
function doSaveAddress(a) {
    var b = jQuery("#county").val();
    if ((b == null || b == "") && jQuery("#detailAddress").val() && jQuery("#city").val() > 0) {
        areaAddress()
    } else {
        updateReceiver = false;
        jQuery("#confirm_address").attr("disabled", "true");
        doSaveOrUpdateLocation(a)
    }
}
function doSaveOrUpdateLocation(b) {
    if (!validateLocation()) {
        jQuery("#confirm_address").removeAttr("disabled");
        return
    }
    var a = getReceiverParam();
    if (!a) {
        a = ""
    }
    showWaitInfo("正在保存收货地址，请等待。。。", b);
    jQuery.post("/checkout/address/saveOrUpdateReceiver.do", a, afterSaveOrUpdateLocation)
}
function doModifyAddress() {
    updateReceiver = true;
    controlSubmitBtnDisplay();
    if (map_load == 1) {
        YHDMapPlaceSelector.initDefaultCheckedStatus()
    } else {
        YHDPlaceSelector.initDefaultCheckedStatus()
    }
}
function popQueryWindow() {
    var a = "/checkout/address/openQueryPlacePage.do";
    jQuery.get(a, null,
    function(b) {
        YHD.popwin(b, 472, 377);
        jQuery("#yhd_pop_win").bgiframe();
        jQuery(window).scroll(function() {
            jQuery("#yhd_pop_win").css({
                top: jQuery(document).scrollTop() + jQuery(window).height() - jQuery("#yhd_pop_win").height() - 150
            })
        })
    })
}
function areaAddress() {
    var a = jQuery("#detailAddress").val();
    if ((currDetailAddress != a && jQuery("#city").val() != 0) || (cityChange == 1)) {
        if (map_load == 1 && isPopMap() && manyFourPlace != 2) {
            var b = jQuery("#detailAddress").val();
            if (b && b != "") {
                cityChange = 0;
                checkDteailAddress();
                mapReturnResult("so")
            }
        }
    }
}
function searchAreaBySo() {
    var f = jQuery("#province").val();
    var b = jQuery("#city").val();
    var a = splitLatlng(latlng);
    var h = parseFloat(a[0]);
    var e = parseFloat(a[1]);
    var d = jQuery("#detailAddress").val();
    var c = "/checkout/address/ajaxGetPlaceCodeBySo.do";
    var g = {
        provinceId: f,
        cityId: b,
        lat: h,
        lng: e,
        dteailAdress: d
    };
    jQuery.post(c, g,
    function(i) {
        if (i && i.message == "success" && i.data) {
            var k = '<option value="' + i.data.countyId + '" postcode="' + i.data.postCode + '" selected></option>';
            var j = '<option value="' + i.data.areaId + '" postcode="' + i.data.postCode + '" selected></option>';
            if (isBigCity()) {
                jQuery("#county").html(k)
            }
            jQuery("#area").html(j);
            jQuery("#postCode").val(i.data.postCode)
        } else {
            popMapWindow()
        }
    },
    "json")
}
var currDetailAddress = "";
function getCurrAddress() {
    currDetailAddress = jQuery("#detailAddress").val()
}
var isInAddressArea = true;
function listenMouseArea() {
    jQuery("#addressContent").mouseout(function() {
        isInAddressArea = false
    });
    jQuery("#addressContent").mouseover(function() {
        isInAddressArea = true
    })
}
function checkDteailAddress() {
    var h = jQuery("#province").find("option:selected").text();
    var e = jQuery("#city").find("option:selected").text();
    var a = jQuery("#county").find("option:selected").text();
    var d = jQuery("#detailAddress").val();
    if (isBigCity()) {
        var c = e;
        var g = h + e + d
    } else {
        var c = a;
        var g = h + e + a + d
    }
    var b = "/checkout/address/ajaxCheckDetailAddress.do";
    var f = {
        r: Math.round(),
        regional: c,
        dteailAdress: g
    };
    jQuery.post(b, f,
    function(i) {
        if (i && i.message == "success" && i.data) {} else {
            jQuery("#addressWarnning").html('<p style="padding:10px 0 0 70px;font-weight:bold;">您填写的<strong style="color:#f00;">' + d + '</strong>可能不在<strong style="color:#f00;">' + c + "</strong>，建议您仔细核实,您可以保存这个收货地址并正常提交订单</p>");
            setTimeout("cancelWarn()", 5000)
        }
    },
    "json")
}
function cancelWarn() {
    jQuery("#addressWarnning").html("")
}
function popMapWindow() {
    if (map_load == 1 && isPopMap() && manyFourPlace != 2) {
        mapReturnResult("call")
    }
}
function mapReturnResultCallBack() {
    if (mapResult != null || mapResult.length > 0) {
        if (mapResult.length > 1) {
            var a = "/checkout/address/openQueryMapPage.do";
            jQuery.get(a, null,
            function(b) {
                YHD.popwin(b, 820, 485);
                jQuery("#yhd_pop_win").bgiframe();
                jQuery(window).scroll(function() {
                    jQuery("#yhd_pop_win").css({
                        top: jQuery(document).scrollTop() + jQuery(window).height() - jQuery("#yhd_pop_win").height() - 150
                    })
                })
            })
        } else {
            if (mapResult.length == 1) {
                ajaxGetPlaceCode()
            }
        }
    } else {
        toggleAddressModel();
        jQuery("#areaMessage").html("为了能准确配送您的订单，请选择您所在的详细地区！")
    }
}
function refreshPlace(b, e, c, d, a) {
    if (map_load == 1) {
        YHDMapPlaceSelector.updateDefaultCheckedStatus(b, e, c, d)
    } else {
        YHDPlaceSelector.updateDefaultCheckedStatus(b, e, c, d)
    }
    jQuery("#postCode").val(formatToString(a))
}
function showYes(b) {
    var a = "<img src='/images/yes.gif'/>";
    jQuery("#" + b).html(a);
    jQuery("#" + b).removeClass("red")
}
function setUpdated() {
    updated = true
}
function checkReceiverName() {
    var a = jQuery("#receiverName").val();
    if (a.trim() == "") {
        jQuery("#receiverNameDesc").html("请输入收货人姓名");
        jQuery("#receiverNameDesc").addClass("red");
        return
    } else {
        if (a.mylength() > 12) {
            jQuery("#receiverNameDesc").html("收货人姓名 不能超过12个字符或6个汉字");
            jQuery("#receiverNameDesc").addClass("red");
            return
        }
    }
    showYes("receiverNameDesc")
}
function checkAddress() {
    var a = jQuery("#detailAddress").val();
    if (a.trim() == "") {
        jQuery("#detailAddressDesc").html("请输入收货地址");
        jQuery("#detailAddressDesc").addClass("red");
        return
    } else {
        if (a.length > 100) {
            jQuery("#detailAddressDesc").html("收货地址 不能超过100个字符或50个汉字");
            jQuery("#detailAddressDesc").addClass("red");
            return
        }
    }
    showYes("detailAddressDesc")
}
function checkPhoneAndCell() {
    var a = jQuery("#phone").val();
    var b = jQuery("#mobile").val();
    if (a == "" && b == "") {
        jQuery("#cell_desc").html("手机和电话不能同时为空");
        jQuery("#cell_desc").addClass("red");
        return
    } else {
        if (b != "") {
            b = b.trim();
            if (checkMobile(b)) {
                jQuery("#cell_desc").html("手机号码格式不正确，请输入正确的手机号码");
                jQuery("#cell_desc").addClass("red");
                return
            }
        }
        if (a != "") {
            a = a.trim();
            var c = /^((\d{3,4})-)?(\d{7,8})(-(\d{1,6}))?$/;
            if (!a.match(c)) {
                jQuery("#cell_desc").html("电话格式不正确");
                jQuery("#cell_desc").addClass("red");
                return
            }
        }
    }
    showYes("cell_desc")
}
function checkPostcode() {
    var a = jQuery("#county").val();
    var b = jQuery("#postCode").val();
    if (a == 0 || b == "") {
        jQuery("#pc_desc").html("邮政编码和县区不匹配");
        return false
    }
    var c = /^\d{6}$/g;
    if (!b.match(c)) {
        jQuery("#pc_desc").html("邮政编码格式不正确");
        return false
    }
    jQuery("#pc_desc").html('<img src="/images/yes.gif"/>')
}
function checkTextValid(c) {
    if (c == null || c.length == 0) {
        return false
    }
    var b = /[\"\'-,.()-,.，。（）\\]/gi;
    var d = c.replace(b, "");
    d = d.replace(/\s/g, "");
    var a = /[\"\'<>,.\/:&*^%$#@!?\\]/;
    if (d == null || d.length == 0) {
        return false
    } else {
        if (a.exec(c)) {
            return false
        } else {
            return true
        }
    }
}
function updateSelectAddress(a) {
    backGoogleMap();
    var b = jQuery("div.row :radio:checked");
    if (b.size() > 0) {
        jQuery("#receiverID").val(b.val())
    } else {
        jQuery("#receiverID").val(0)
    }
    var c = jQuery("#receiverID").val();
    proUpdateSelectAddress(a, c)
}
function proUpdateSelectAddress(a, b) {
    if (b == 0) {
        create = true;
        jQuery("#receiverNameDesc").val("不能超过12个字符或6个汉字");
        jQuery("#cell_desc").val("手机和电话至少有一项必填");
        jQuery("#detailAddressDesc").val("不能超过100个字符或50个汉字");
        jQuery("#default_province_id").val("");
        jQuery("#default_city_id").val("");
        jQuery("#default_county_id").val("");
        jQuery("#province").val(0);
        jQuery("#city").val(0);
        jQuery("#county").val(0);
        jQuery("#receiverName").val("");
        jQuery("#detailAddress").val("");
        jQuery("#postCode").val("");
        jQuery("#mobile").val("");
        jQuery("#phone").val("");
        if (map_load == 1) {
            YHDMapPlaceSelector.clearDefaultCheckedStatus()
        } else {
            YHDPlaceSelector.clearDefaultCheckedStatus()
        }
        if (pageAddressProvinceIdV2 !== null && pageAddressProvinceIdV2 > 0) {
            jQuery("#province").attr("value", pageAddressProvinceIdV2);
            jQuery("#province").change()
        }
        return
    } else {
        ajaxGetGoodReceiverById(b)
    }
}
function linkToAlipay() {
    jQuery.post("/alipay/alipayAddress.do", {
        nowUrl: document.location.href
    },
    linkToAlipayFinish)
}
function linkToAlipayFinish(a) {
    window.open(a)
}
function ajaxGetGoodReceiverById(c) {
    var a = "/checkout/address/ajaxGetGoodReceiverById.do";
    var b = {
        id: c,
        rd: Math.random()
    };
    jQuery.get(a, b,
    function(d) {
        if (d.message == "success") {
            var e = d.data;
            if (map_load == 1) {
                YHDMapPlaceSelector.updateDefaultCheckedStatus(e.provinceId, e.cityId, e.countyId, e.areaId)
            } else {
                YHDPlaceSelector.updateDefaultCheckedStatus(e.provinceId, e.cityId, e.countyId, e.areaId)
            }
            jQuery("#receiverName").val(formatToString(e.receiverName));
            jQuery("#detailAddress").val(formatToString(e.address1));
            jQuery("#postCode").val(formatToString(e.postCode));
            jQuery("#mobile").val(formatToString(e.receiverMobile));
            jQuery("#phone").val(formatToString(e.receiverPhone));
            jQuery("#email").val(formatToString(e.receiverEmail))
        } else {
            window.location = "/product/cart.do?action=view"
        }
    },
    "json")
}
function afterSaveOrUpdateLocation(c) {
    jQuery("#confirm_address").removeAttr("disabled");
    if (c != null && parseInt(c) == -99) {
        clearWaitInfo();
        alert("亲爱的用户，您输入的手机或电话号码格式不正确，请重新输入!");
        var a = jQuery("#mobile").val();
        if (a != null && jQuery.trim(a).length > 0) {
            jQuery("#mobile").select()
        } else {
            jQuery("#phone").select()
        }
    } else {
        if (c != null && parseInt(c) == -97) {
            clearWaitInfo();
            alert("亲爱的用户，您当前选择的省，市，区/县等地址信息不正确，请重新选择!");
            toggleAddressModel();
            jQuery("#areaMessage").html("为了能准确配送您的订单，请选择您所在的详细地区！")
        } else {
            if (c != null && c.search("theOnlyDecisionMarksASuccessful") == -1) {
                if (c.indexOf("checkoutAjaxErrorFlg") != -1) {
                    window.location.href = "/product/cart.do?action=view"
                } else {
                    clearWaitInfo();
                    jQuery("#errorMsgDisplayDiv").html(c);
                    doShowErrors()
                }
                return
            } else {
                jQuery("#errorMsgDisplayDiv").html("")
            }
            if (!redirectIfNotLogin(c)) {
                return false
            }
            flow_step = 2;
            renderUI();
            clearWaitInfo();
            var b = genShowReceiverHtml();
            jQuery("#receiverInfoSpan").html(b);
            jQuery("#receiver_buffer_window").html(c)
        }
    }
}
function genShowReceiverHtml() {
    var c = "";
    var f = jQuery("#receiverName").val();
    var d = jQuery("#province").find("option:selected").text();
    var e = jQuery("#city").find("option:selected").text();
    var h = jQuery("#county").find("option:selected").text();
    var l = jQuery("#county").val();
    var k = jQuery("#area").val();
    var b = "";
    if (l && k && (l == k || k == 0)) {
        b = ""
    } else {
        b = jQuery("#area").find("option:selected").text()
    }
    var g = jQuery("#detailAddress").val();
    var j = jQuery("#postCode").val();
    var a = jQuery("#mobile").val();
    var i = jQuery("#phone").val();
    c += " " + d + " " + e + " ";
    if (!isBigCity()) {
        c += h + " ";
        if (h != b) {
            c += b
        }
    }
    c += " " + g + " " + f + " " + a + " " + i;
    return c
}
function checkemail() {
    var a = jQuery("#email").val();
    a = a.trim();
    if (a == "") {
        jQuery("#emailmesdiv").html("email不能为空");
        jQuery("#emailmesdiv").addClass("red");
        return
    }
    if (!CheckEmail(a)) {
        jQuery("#emailmesdiv").html("email格式不正确");
        jQuery("#emailmesdiv").addClass("red");
        return
    }
    jQuery("#emailmesdiv").html("<img src='/images/yes.gif'/>")
}
function CheckEmail(a) {
    var a = a;
    var b = /^([a-zA-Z0-9._-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    flag = b.test(a);
    if (!flag) {
        return false
    }
    return true
}
function validateLocation() {
    var d = jQuery("#receiverID").val();
    var h = jQuery("#receiverName").val().trim();
    var b = jQuery("#detailAddress").val().trim();
    var m = jQuery("#postCode").val().trim();
    var j = jQuery("#phone").val().trim();
    var a = jQuery("#mobile").val().trim();
    var l = null;
    if (jQuery("#email") && jQuery("#email").val()) {
        l = jQuery("#email").val().trim()
    }
    var o = jQuery("#city").val();
    var n = jQuery("#province").val();
    if (n == null) {
        n = 1
    }
    var f = jQuery("#county").val();
    if (d == -1) {
        alert("请选择收货地址.");
        return false
    } else {
        if (d == 0) {
            create = true
        }
    }
    if (h == "") {
        alert("请输入收货人姓名.");
        jQuery("#receiverName").focus();
        return false
    } else {
        if (h.mylength() > 12) {
            alert("收货人姓名 不能超过12个字符或6个汉字");
            jQuery("#receiverName").focus();
            return false
        } else {
            if (checkTextValid(h) == false) {
                alert("收货人姓名不能为空,并且不能包含特殊字符!");
                jQuery("#receiverName").select();
                return false
            }
        }
    }
    if (b == "") {
        alert("请输入收货地址.");
        jQuery("#detailAddress").focus();
        return false
    } else {
        if (len(b) > 100) {
            alert("收货地址 不能超过100个字符或50个汉字");
            jQuery("#detailAddress").focus();
            return false
        } else {
            if (checkTextValid(b) == false) {
                alert("收货地址不能为空,并且不能包含特殊字符!");
                jQuery("#detailAddress").select();
                return false
            }
        }
    }
    if (n == 0 || o == 0 || f == 0) {
        alert("请选择地区.");
        return false
    }
    var e = 0;
    if (jQuery("#area").size() > 0) {
        e = jQuery("#area").val()
    }
    if (e == null || parseInt(e) == 0) {
        if (jQuery("#area").size() > 0 && jQuery("#area option").size() > 0) {
            alert("请选择一个四级区域.");
            return false
        }
    }
    if (j == "" && a == "") {
        alert("手机和电话不能同时为空.");
        jQuery("#mobile").focus();
        return false
    } else {
        if (a != "") {
            a = a.trim();
            var c = /^\d{11}$/g;
            if (!a.match(c)) {
                alert("手机号码格式不正确，请输入11位数字.");
                jQuery("#mobile").focus();
                return false
            }
        }
        if (j != "") {
            j = j.trim();
            var c = /^((\d{3,4})-)?(\d{7,8})(-(\d{1,6}))?$/;
            if (!j.match(c)) {
                alert("电话格式不正确.");
                jQuery("#phone").focus();
                return false
            }
        }
    }
    if (l) {
        if (l == "") {
            alert("email不能为空");
            jQuery("#email").focus();
            return false
        }
        if (!CheckEmail(l)) {
            alert("email格式不正确");
            jQuery("#email").focus();
            return false
        }
    }
    if (n != pageAddressProvinceIdV2) {
        if (jQuery("#checkoutAddressChangeCity").size() > 0) {
            YHD.popwin(jQuery("#checkoutAddressChangeCity").html(), "475px", "209px")
        }
        return false
    }
    if (!updated) {
        var i = jQuery("#oprovinceID").val();
        var g = jQuery("#ocityID").val();
        var k = jQuery("#ocountyID").val();
        if (i != n || g != o || k != f) {
            updated = true
        }
    }
    return true
}
function getReceiverParam() {
    var c = jQuery("#new_address").attr("checked") == true;
    var d = jQuery("#receiverID").val();
    var k = "";
    var g = jQuery("#receiverName").val().trim();
    var b = jQuery("#detailAddress").val().trim();
    var l = jQuery("#postCode").val().trim();
    var h = jQuery("#phone").val().trim();
    var a = jQuery("#mobile").val().trim();
    var j = null;
    if (jQuery("#email") && jQuery("#email").val()) {
        j = jQuery("#email").val().trim()
    }
    var n = jQuery("#city").val();
    var m = jQuery("#province").val();
    var f = jQuery("#county").val();
    var e = jQuery("#area").val();
    var o = "";
    if (c) {
        o += "receiver.recordName=" + encodeURIComponent(k) + "&action=create";
        var i = jQuery("#saveMobile");
        if (i && i.checked) {
            o += "&saveMobile=true"
        }
    } else {
        o += "receiver.id=" + d + "&action=update"
    }
    if (e == null || e == 0) {
        e = f
    }
    o += "&receiver.receiverName=" + encodeURIComponent(g) + "&receiver.address1=" + encodeURIComponent(b) + "&receiver.postCode=" + l + "&receiver.phone=" + h + "&receiver.mobile=" + a + "&receiver.provinceID=" + m + "&receiver.cityID=" + n + "&receiver.countyID=" + f;
    o += "&receiver.areaID=" + e;
    o += "&rd=" + Math.random();
    if (j) {
        o = o + "&email=" + j
    }
    return o
}
function addAlipayAddree(c, b, d, a) {
    jQuery("#new_address").attr("checked", "checked");
    proUpdateSelectAddress(null, 0);
    jQuery("#receiverName").val(b);
    jQuery("#detailAddress").val(c);
    jQuery("#mobile").val(d);
    jQuery("#phone").val(a)
}
function myAddressHideShow() {
    if (jQuery("div.row:visible").size() > 5) {
        jQuery("div.row:gt(4)").hide();
        jQuery("#showAddress").html("【显示所有收货地址】 &nbsp;&nbsp;")
    } else {
        if (jQuery("div.row:visible").size() <= 5 && jQuery("div.row").size() > 5) {
            jQuery("div.row:gt(4)").show();
            jQuery("#showAddress").html("【隐藏部分收货地址】 &nbsp;&nbsp;")
        }
    }
}
function myAddressHover() {
    jQuery("div.row").hover(function() {
        if (!jQuery(this).hasClass("row_hover")) {
            jQuery(this).addClass("row_hover");
            jQuery(this).find("span").show()
        }
    },
    function() {
        if (jQuery(this).hasClass("row_hover")) {
            jQuery(this).removeClass("row_hover");
            jQuery(this).find("span").hide()
        }
    })
}
function edit(a) {
    backGoogleMap();
    var b = jQuery("div.row_hover input");
    if (b.size() > 0) {
        b.attr("checked", true);
        jQuery("#receiverID").val(b.val())
    } else {
        jQuery("#receiverID").val(0)
    }
    var c = jQuery("#receiverID").val();
    proUpdateSelectAddress(a, c)
}
function backGoogleMap() {
    var a = jQuery("div.row :radio:checked");
    if (google_config == 1 && a.val() > 0) {
        if (map_load == 2) {
            map_load = 1
        }
        jQuery("#areaMessage").hide();
        if (map_load == 1) {
            YHDMapPlaceSelector.initDefaultCheckedStatus()
        } else {
            YHDPlaceSelector.initDefaultCheckedStatus()
        }
    }
}
function checkMobile(b) {
    if (b != "") {
        var h = /^13\d{5,9}$/;
        var g = /^153\d{4,8}$/;
        var f = /^159\d{4,8}$/;
        var e = /^0\d{10,11}$/;
        var d = /^150\d{4,8}$/;
        var c = /^158\d{4,8}$/;
        var a = /^15\d{5,9}$/;
        var i = false;
        if (h.test(b)) {
            i = true
        }
        if (g.test(b)) {
            i = true
        }
        if (f.test(b)) {
            i = true
        }
        if (e.test(b)) {
            i = true
        }
        if (d.test(b)) {
            i = true
        }
        if (c.test(b)) {
            i = true
        }
        if (a.test(b)) {
            i = true
        }
        if (!i) {
            return false
        }
    }
};
var geocoder;
var map;
var myOptions;
var mapResult;
var latlng;
function initialize() {
    try {
        geocoder = new google.maps.Geocoder()
    } catch(a) {}
    var b = new google.maps.LatLng(31.2, 121.4);
    myOptions = {
        zoom: 8,
        center: b,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
}
function mapReturnResult(b) {
    initialize();
    var a = jQuery("#province").find(":selected").text();
    var f = jQuery("#city").find(":selected").text();
    var e = "";
    if (!isBigCity()) {
        e = jQuery("#county").find(":selected").text()
    }
    var d = jQuery("#detailAddress").val();
    var c = a + f + e + d;
    if (geocoder) {
        geocoder.geocode({
            address: c
        },
        function(h, g) {
            if (g == google.maps.GeocoderStatus.OK) {
                mapResult = h;
                if (h.length > 0) {
                    latlng = h[0].geometry.location
                }
                if (b == "call") {
                    mapReturnResultCallBack()
                } else {
                    if (b == "so") {
                        searchAreaBySo()
                    }
                }
            } else {
                if (g == google.maps.GeocoderStatus.ZERO_RESULTS) {
                    toggleAddressModel();
                    jQuery("#areaMessage").html("为了能准确配送您的订单，请选择您所在的详细地区！");
                    mapResult = null
                } else {
                    mapResult = null
                }
            }
        })
    } else {
        mapResult = null
    }
}
function codeAddress() {
    var a = jQuery("#province").find(":selected").text();
    var e = jQuery("#city").find(":selected").text();
    var d = "";
    if (!isBigCity()) {
        d = jQuery("#county").find(":selected").text()
    }
    var c = jQuery("#detailAddress").val();
    var b = a + e + d + c;
    if (!geocoder) {
        initialize()
    }
    if (geocoder) {
        geocoder.geocode({
            address: b
        },
        function(k, h) {
            if (h == google.maps.GeocoderStatus.OK) {
                myOptions.zoom = 12;
                map = new google.maps.Map(document.getElementById("map_content"), myOptions);
                map.setCenter(k[0].geometry.location);
                var g = k.length;
                if (k.length > 9) {
                    g = 9
                }
                for (var j = 0; j < g; j++) {
                    var f = new google.maps.Marker({
                        map: map,
                        position: k[j].geometry.location,
                        title: k[j].formatted_address
                    });
                    showGoogleAddress(k[j].formatted_address, j)
                }
            } else {
                toggleAddressModel();
                jQuery("#areaMessage").html("为了能准确配送您的订单，请选择您所在的详细地区！")
            }
        })
    }
}
function placeMarker(b) {
    var c = new google.maps.LatLng(b);
    var a = new google.maps.Marker({
        position: b,
        map: map
    });
    map.setCenter(b)
}
function splitLatlng(b) {
    $latlng = b.toString();
    $latlng = $latlng.substr(1, $latlng.length - 2);
    var a = $latlng.split(",", 2);
    return a
}
function showGoogleAddress(b, f) {
    var c = document.getElementById("map_info");
    var e = document.createElement("li");
    var a = (f == 0) ? "checked": "";
    var g = b;
    var d = "<label><strong><em>" + (f + 1) + '</em><input name="map_add_line" type="radio" value="' + latlng + '" add="' + g + '" ' + a + "/></strong>" + g + "</label>";
    e.innerHTML = d;
    c.appendChild(e)
}
function selectMapAddress() {
    jQuery(".ap_add strong").html(jQuery("input[name='map_add_line']:checked").attr("add"));
    jQuery(".ap_add").show()
}
function cancelSelect() {
    jQuery(".ap_add").hide();
    jQuery(".ap_add strong").html("")
}
function ajaxGetPlaceCode() {
    if (!latlng || latlng == "") {
        latlng = jQuery("input[name='map_add_line']:checked").val()
    }
    var a = splitLatlng(latlng);
    var g = parseFloat(a[0]);
    var d = parseFloat(a[1]);
    var b = jQuery("#city").val();
    var f = "";
    if (!isBigCity()) {
        f = jQuery("#county").val()
    }
    var c = "/checkout/address/ajaxGetPlaceCodeByLatlng.do";
    var e = {
        cityId: b,
        countyId: f,
        lat: g,
        lng: d
    };
    jQuery.post(c, e,
    function(h) {
        if (h && h.message == "success" && h.data) {
            var j = '<option value="' + h.data.countyId + '" postcode="' + h.data.postCode + '" selected>' + h.data.countyCname + "</option>";
            var i = '<option value="' + h.data.areaId + '" postcode="' + h.data.postCode + '" selected>' + h.data.areaCname + "</option>";
            if (isBigCity()) {
                jQuery("#county").html(j)
            }
            jQuery("#area").html(i);
            jQuery("#postCode").val(h.data.postCode)
        } else {
            toggleAddressModel();
            jQuery("#areaMessage").html("为了能准确配送您的订单，请选择您所在的详细地区！")
        }
    },
    "json")
}
function isPopMap() {
    if (isBigCity()) {
        return true
    } else {
        if (!isBigCity() && manyFourPlace == 1) {
            return true
        } else {
            return false
        }
    }
};
function doModifyPayment(a) {
    updatePayment = true;
    controlSubmitBtnDisplay();
    requestPaymentMethodsEx()
}
function validateUser() {
    var a = "/checkout/confirm/checkoutUser.do?rd=" + Math.random();
    jQuery.ajax({
        type: "get",
        url: a,
        async: false,
        success: function(b) {
            jQuery("#confirm_goods1").hide();
            if (b.data.cheatingLevel == 1) {
                jQuery("#confirm_goods1").show();
                jQuery("#validCodeCheck1").show();
                jQuery("#confirm_goods2").hide()
            }
            if (b.data.cheatingLevel == 2) {
                jQuery("#confirm_goods1").hide()
            }
        }
    })
}
function getPaymentMethods() {
    var a = "/checkout/payselect/requestAllPaymentMethod.do?rd=" + Math.random();
    var b = {};
    jQuery("#paymentListTable").empty();
    jQuery.get(a, b, afterGetPaymentMethods)
}
function requestPaymentMethodsEx() {
    var a = "/checkout/payselect/requestAllPaymentMethod.do?rd=" + Math.random();
    var b = {};
    jQuery("#payment_buffer_window").empty();
    jQuery.get(a, b, afterRequestPaymentMethodsEx)
}
function afterGetPaymentMethods(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    jQuery("#paymentListTable").html(a);
    jQuery("#defaultPaymentDiv").css("display", "none");
    jQuery("#paymentListDiv").css("display", "block");
    if (jQuery("#reSelPaymentMethod").val() == 1 || updatePayment || (jQuery("#needSelectPayment") && jQuery("#needSelectPayment").val() == 1)) {
        jQuery("#paymentListDiv").css("display", "block");
        jQuery("#defaultPaymentDiv").css("display", "none");
        paymentSpecControl = true;
        controlSubmitBtnDisplay()
    } else {
        jQuery("#paymentListDiv").css("display", "none");
        jQuery("#defaultPaymentDiv").css("display", "block");
        jQuery("#paymentMethodSpan").html(jQuery("#paymentMethodName").val())
    }
    clearWaitInfo()
}
function doSavePayment(a) {
    passValueToPay();
    if (!valdiatePaymentMethod()) {
        jQuery("#confirm_payment").removeAttr("disabled");
        return
    }
    updatePayment = false;
    showWaitInfo("正在保存付款方式，请等待。。。", a);
    doSavePaymentMethod()
}
function passValueToPay() {
    jQuery("#checkedBankImg").attr("src", bankImg);
    jQuery("#checkedBankImg").attr("checkedBankGatewayId", bankId);
    jQuery("#checkedBankName").text(bankName);
    jQuery("#gatewayImageStr").val(bankImg);
    jQuery("#confirm_payment").attr("disabled", "true");
    jQuery("#gatewayID").val(bankId)
}
function doSavePaymentMethod() {
    validateUser();
    var a = "/checkout/payselect/confirmPaymentMethod.do?paymentMethodID=" + jQuery("#paymentMethodID").val() + "&paymentGatewayID=" + jQuery("#gatewayID").val();
    var b = jQuery("[name='payInstallmentId']:radio:checked").val();
    if (b != null && b != "") {
        a = a + "&payInstallmentId=" + b
    }
    a = a + "&rd=" + Math.random();
    jQuery.post(a, "", afterSavePaymentMethod)
}
function afterSavePaymentMethod(a) {
    jQuery("#confirm_payment").removeAttr("disabled");
    if (!redirectIfNotLogin(a)) {
        return false
    }
    var b = "<image src='" + jQuery("#gatewayImageStr").val() + '\' align="top" class="fl ml5">';
    if (jQuery("#paymentMethodIDTmp4").attr("checked") == true) {
        jQuery("#paymentMethodSpan").html("<span class='fl'>" + jQuery("#paymentMethodName").val() + "</span>" + b);
        $("#paymessage").show()
    } else {
        jQuery("#paymentMethodSpan").html("<span class='fl'>" + jQuery("#paymentMethodName").val() + "</span>");
        $("#paymessage").hide()
    }
    clearWaitInfo();
    controlSubmitBtnDisplay();
    flow_step = 4;
    renderUI()
}
function doSaveByAccount() {
    var h = 0;
    var b = parseFloat(jQuery("#needPay").html());
    var d = 0;
    var h = 0;
    var f = parseFloat(jQuery("#couponAmount").html());
    var i = 0;
    if (typeof(zhongXinPointsV2) != "undefined") {
        i = zhongXinPointsV2
    }
    var k = 0;
    if (document.getElementById("payZxAmount")) {
        k = document.getElementById("payZxAmount").value;
        if (k != "") {
            k = parseFloat(k)
        }
    }
    if (jQuery("#balance")) {
        d = parseFloat(jQuery("#balance").html());
        var g = jQuery("#payByAccount").val();
        if (g == "") {
            g = "0"
        }
        var c = /\d+\.?\d*/g;
        if (!g.match(c)) {
            alert("请输入数字.");
            jQuery("#payByAccount").empty();
            jQuery("#payByAccount").focus();
            return false
        }
        h = parseFloat(g);
        if (h > d) {
            alert("帐户余额不足.");
            jQuery("#payByAccount").focus();
            return false
        }
        if (k > i) {
            alert("中信帐户余额不足.");
            jQuery("#payZxAmount").focus();
            return false
        }
    }
    var e = jQuery("#couponNumber").val().trim();
    var a = "/checkout/payselect/savePaybyAccount.do";
    var j = "payByAccount=" + h + "&couponNumber=" + e + "&payZxAmount=" + k;
    jQuery.post(a, j, afterPaybyAccount)
}
function afterPaybyAccount(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    if (a != "") {
        alert(a)
    } else {
        jQuery("#zh").css("display", "none");
        doGetAmountList()
    }
}
function getWLTPoints() {
    if (hasPingAnCookie && hasPingAnCookie == 1) {
        jQuery.post("/pingan/queryPointsAmount.do?rd=" + Math.random(), "", updatePoints)
    }
}
function updatePoints(d) {
    if (!redirectIfNotLogin(d)) {
        return false
    }
    var i = d;
    if (i) {
        var c = i.split("=");
        if (c.length > 0) {
            var j = c[0];
            if (j == 1) {
                var a = c[1];
                var g = a.split(",");
                var h = g[0];
                var f = g[1];
                var b = jQuery("#wltPoints");
                if (b.size() > 0) {
                    b.html(h);
                    jQuery("#wltPoints").show();
                    jQuery("#wltPoints_waiting").hide()
                }
                var e = jQuery("#wltPoints2");
                if (e.size() > 0) {
                    e.html(h);
                    jQuery("#wltPoints2").show();
                    jQuery("#wltPoints2_waiting").hide()
                }
            }
        }
    }
}
function afterRequestPaymentMethodsEx(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    jQuery("#payment_buffer_window").html(a);
    getWLTPoints();
    clearWaitInfo();
    initPayMethodPageEvent()
}
function refreshPM() {
    document.cookie = "netpaycode=;path=/";
    doModifyPayment()
}
function valdiatePaymentMethod() {
    var f = jQuery("#paymentType").val();
    if (f == "") {
        alert("请选择付款方式.");
        return false
    }
    var g = jQuery("#paymentMethodID").val();
    if (g == "") {
        alert("请选择付款方式.");
        return false
    }
    var e = document.getElementsByName("paymentMethodIDTmp");
    if (!e) {
        alert("请选择付款方式.");
        return false
    }
    var h = false;
    if (e.length > 0) {
        for (var d = 0; d < e.length; d++) {
            if (e[d].checked) {
                h = true
            }
        }
    }
    if (!h) {
        alert("请选择付款方式.");
        return false
    }
    if (f == 4) {
        var c = jQuery("#bank").val();
        if (c == 0) {
            alert("请选择转账的银行.");
            return false
        }
    }
    if (f == 1) {
        var a = jQuery("[name='pay_gateway_bank']:radio:checked");
        if (a.size() == 0) {
            jQuery("#tableBankList").jqmShow();
            jQuery("#tableBankErrorTip").html("尊敬的用户,您需要选择一个支付平台或网银!").fadeIn();
            return false
        } else {
            jQuery("#tableBankList").jqmHide();
            jQuery("#tableBankErrorTip").empty().hide()
        }
    }
    if (f == 7) {
        var b = jQuery("[name='payInstallmentId']:radio:checked");
        if (b.size() == 0) {
            alert("请选择分期付款期数");
            return false
        }
    }
    return true
}
function showInstallmentRule(c, a, b) {
    var d = jQuery("#installmentRule");
    d.html('<font color="red">' + Round(c * (1 + b / 100) / a, 2) + '</font>元 Ⅹ <font color="red">' + a + "</font> 期（月）");
    d.show()
}
function notePayGateway(c) {
    jQuery("#gatewayID").val(c.id);
    jQuery("#gatewayImageStr").val(c.value);
    jQuery("#paymentMethodIDTmp4").click();
    jQuery("#tableBankList.ap_netpay li.on_checked").removeClass("on_checked");
    jQuery(c).parent().addClass("on_checked");
    var e = jQuery(c);
    var d = e.attr("bankName");
    var a = e.attr("id");
    var b = e.val();
    fillValueForPay(d, a, b);
    if (jQuery("#checkedBankImg").size() > 0 && jQuery("#checkedBankName").size() > 0) {
        jQuery("#checkedBankImg").attr("checkedBankGatewayId", a);
        jQuery("#checkedBankImg").attr("src", b);
        jQuery("#checkedBankName").text(d);
        jQuery("#checkedBankDiv").show();
        jQuery("#notCheckedBankDiv").hide()
    }
    jQuery("#tableBankErrorTip").fadeOut()
}
function dealSavePayment(a) {
    var d = jQuery("#" + a.id).attr("vMethodName");
    var c = jQuery("#" + a.id).attr("vMethodId");
    var b = jQuery("#" + a.id).attr("vMethodType");
    jQuery("#paymentMethodName").val(d);
    jQuery("#paymentMethodID").val(c);
    jQuery("#paymentType").val(b);
    jQuery("input[name='payGatewayId']:radio:checked").attr("checked", false);
    jQuery("input[name='payInstallmentId']:radio:checked").attr("checked", false);
    jQuery("#gatewayID").val("");
    jQuery("#gatewayImageStr").val("")
}
function selectInstallmentBank(a) {
    jQuery("#paymentMethodIDTmp7").click();
    jQuery("input[name='pay_gateway_bank']:radio:checked").attr("checked", false)
}
function dealSavePayment2(a) {
    var d = jQuery("#" + a.id).attr("vMethodName");
    var c = jQuery("#" + a.id).attr("vMethodId");
    var b = jQuery("#" + a.id).attr("vMethodType");
    jQuery("#paymentMethodName").val(d);
    jQuery("#paymentMethodID").val(c);
    jQuery("#paymentType").val(b);
    jQuery("input[name='payInstallmentId']:radio:checked").attr("checked", false)
}
function dealSavePayment3(a) {
    var d = jQuery("#" + a.id).attr("vMethodName");
    var c = jQuery("#" + a.id).attr("vMethodId");
    var b = jQuery("#" + a.id).attr("vMethodType");
    jQuery("#paymentMethodName").val(d);
    jQuery("#paymentMethodID").val(c);
    jQuery("#paymentType").val(b);
    jQuery("#gatewayID").val("");
    jQuery("#gatewayImageStr").val("")
}
function initPopBankListWin() {
    if (jQuery("#tableBankList").size() > 0) {
        jQuery("#tableBankList").bgiframe();
        jQuery("#tableBankList").jqm({
            overlay: 10,
            overlayClass: "pop_win_bg",
            modal: true,
            toTop: true
        }).jqmAddClose(".popwinClose");
        jQuery(window).scroll(function() {
            jQuery("#tableBankList").css({
                top: jQuery(document).scrollTop() + jQuery(window).height() - jQuery("#tableBankList").height() - 50
            })
        })
    }
}
function popBankListWin() {
    if (jQuery("#tableBankList").size() > 0) {
        jQuery("#tableBankList").jqmShow()
    }
    return false
}
function showBankListPopWin(a) {
    if (a != null && a == 1) {
        var b = jQuery(":radio[name='pay_gateway_bank']:checked");
        if (b != null && b.size() > 0) {} else {
            popBankListWin()
        }
    } else {
        jQuery("#paymentMethodIDTmp4").click();
        popBankListWin()
    }
}
var bankId;
var bankName;
var bankImg;
var paymentMethodId;
function initPayMethodPageEvent() {
    jQuery(":radio[name='paymentMethodIDTmp']").click(function() {
        jQuery("#paymentMethodList li").removeClass("select");
        jQuery(this).parent().addClass("select")
    });
    var g = jQuery(":radio[name='pay_gateway_bank']:checked");
    if (g != null && g.size() > 0) {
        var f = g.attr("bankName");
        var b = g.val();
        var a = g.attr("id");
        fillValueForPay(f, a, b);
        if (jQuery("#checkedBankImg").size() > 0 && jQuery("#checkedBankName").size() > 0) {
            jQuery("#checkedBankImg").attr("src", b);
            jQuery("#checkedBankImg").attr("checkedBankGatewayId", a);
            jQuery("#checkedBankName").text(f);
            jQuery("#gatewayImageStr").val(b)
        }
    }
    var e = jQuery(":radio[name='paymentMethodIDTmp']:checked");
    if ((e == null || e.size() == 0)) {
        var c = jQuery(":radio[name='paymentMethodIDTmp']:eq(0)");
        var d = c.attr("id");
        if (d == "paymentMethodIDTmp4" && (g == null || g.size() == 0)) {} else {
            c.click()
        }
    }
    initPopBankListWin()
}
function fillValueForPay(c, a, b) {
    bankName = c;
    bankId = a;
    bankImg = b
};
var submitted = false;
function submitWlt(a) {
    if (submitted) {
        YHD.alert("正在处理支付请求，请不要重复请求");
        return
    }
    window.location = "/pingan/redeemPoint.do?orderCode=" + a;
    submitted = true
}
function submitWlt2(a, b) {
    if (submitted) {
        alert("正在处理支付请求，请不要重复请求");
        return
    }
    submitted = true;
    window.location.replace("/product/confirmOrder!selectGateWay.do?paymentMethodId=" + b + "&myOrderId=" + a)
}
function doPay(c, b, a) {
    $("#currGateWayReturnUrl").val(a);
    window.open("/product/confirmOrder!selectGateWay.do?gateWayId=" + c + "&myOrderId=" + b);
    YHD.popwinId("pay_wait_win", "close")
}
function finishPay() {
    var a = $("#currGateWayReturnUrl").val();
    if (a && a != "") {
        window.location.href = "/"
    } else {
        $(".close").click()
    }
}
function problemPay(a) {
    window.location.href = "/product/confirmOrder!payProblem.do?rd=" + Math.random() + "&myOrderId=" + a
};
function placeOrder(b) {
    if (hasErrors()) {
        doShowErrors();
        return
    }
    if (attachedObjectsSize > 0 && attached != true) {
        alert("请保存附加信息");
        return
    }
    var a = (jQuery("#remainToPay") && jQuery("#remainToPay").val() <= 0);
    var c = jQuery("#paymentListDiv") && jQuery("#paymentListDiv").css("display") != "none";
    if (hasErrors()) {
        doShowErrors();
        return
    }
    waitForSubmitOrder();
    showWaitInfo("正在提交订单，请等待。。。", b);
    if (needIntegralV2 > 0) {
        jQuery.post("/checkout/confirm/checkUserPoint.do?rd=" + Math.random(), "", afterCheckUserPoint)
    } else {
        checkStock()
    }
}
function checkStock() {
    jQuery.post("/checkout/confirm/checkAllOrders.do?rd=" + Math.random(), "", afterCheckStock)
}
function afterCheckStock(c) {
    if (!redirectIfNotLogin(c)) {
        return false
    }
    var d = c;
    if (d) {
        d = d.trim()
    }
    if (d && d == "sessionOrderTimeOut") {
        alert("由于您长时间没有确认订单导致订单信息超时，请返回到购物车重新提交订单。");
        window.location = "/product/cart.do?action=view";
        return
    }
    if (d && d.length > 10) {
        unWaitForSubmitOrder();
        jQuery("#errorMsgDisplayDiv").html(c);
        doShowErrors();
        clearWaitInfo()
    } else {
        var a = "";
        a += "&orderID=1";
        var e = jQuery("#rdCheck").val();
        var f = jQuery("#gatewayID").val();
        var b = "/product/confirmOrder!saveOrder2.do?rdCheck=" + e + "&rd=" + Math.random() + "&gateWayId=" + f;
        b += a;
        clearWaitInfo();
        window.location = b
    }
}
function doGetAmountList() {
    jQuery.post("/checkout/confirm/getOrderUnit.do?rd=" + Math.random(), "", afterGetProductList)
}
function afterGetProductList(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    jQuery("#amountListDiv").html(a)
}
var chooseInvoiceType = 2;
function doSaveInvoice() {
    var m = "";
    var c = jQuery("#needInvoice");
    var f = 0;
    var k = true;
    if (jQuery("#needInvoice").attr("checked") == true) {
        var j = "";
        var h = "";
        j = jQuery("#headType option:selected").val();
        if (j == "-1") {
            j = jQuery("#normal_head").val()
        }
        var d = jQuery("input[name=invoiceType][checked]").val();
        if (chooseInvoiceType == 2) {
            if (j.trim() != "") {
                if (j.length > 50) {
                    alert("发票抬头不能超过50个字符或者25个汉字");
                    jQuery("#normal_head").focus();
                    k = false
                }
                h = jQuery("#invoiceContent").val();
                f = 1;
                if (m != "") {
                    m += "&"
                }
                m += "needInvoice=" + f + "&invoiceTitle=" + encodeURI(j) + "&invoiceContent=" + encodeURI(h) + "&invoiceType=2"
            } else {
                if (jQuery("#needInvoice").attr("checked") == true) {
                    alert("请填写您索取发票的抬头")
                }
                k = false
            }
        } else {
            if (chooseInvoiceType == 3) {
                var b = jQuery("#vatCompanyNameText").val();
                var i = jQuery("#vatTaxpayerText").val();
                var a = jQuery("#vatCompanyAddressText").val();
                var g = jQuery("#vatCompanyPhoneText").val();
                var l = jQuery("#vatBankAccountText").val();
                var e = jQuery("#vatDeliveryAddressText").val();
                if (b.trim() == "") {
                    jQuery("#vatCompanyName").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatCompanyName").attr("class", "none")
                }
                if (i.trim() == "") {
                    jQuery("#vatTaxpayer").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatTaxpayer").attr("class", "none")
                }
                if (a.trim() == "") {
                    jQuery("#vatCompanyAddress").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatCompanyAddress").attr("class", "none")
                }
                if (g.trim() == "") {
                    jQuery("#vatCompanyPhone").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatCompanyPhone").attr("class", "none")
                }
                if (l.trim() == "") {
                    jQuery("#vatBankAccount").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatBankAccount").attr("class", "none")
                }
                if (e.trim() == "") {
                    jQuery("#vatDeliveryAddress").attr("class", "wrong");
                    k = false;
                    return
                } else {
                    jQuery("#vatDeliveryAddress").attr("class", "none")
                }
                f = 1;
                if (m != "") {
                    m += "&"
                }
                m += "needInvoice=" + f + "&vatCompanyName=" + encodeURI(b) + "&vatTaxpayer=" + encodeURI(i) + "&vatCompanyAddress=" + encodeURI(a) + "&vatCompanyPhone=" + encodeURI(g) + "&vatBankAccount=" + encodeURI(l) + "&vatDeliveryAddress=" + encodeURI(e) + "&invoiceType=3"
            }
        }
    }
    if (k) {
        if (m != "") {
            m += "&"
        }
        invoceControl = false;
        controlSubmitBtnDisplay();
        m += "&rd=" + Math.random();
        jQuery("#next").attr("disabled", true);
        jQuery.post("/product/confirmOrder!saveInvoice.do", m, afterSaveInvoice)
    }
}
function afterSaveInvoice(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    if (a != null) {
        document.getElementById("rdCheck").value = a
    }
    submitOrder()
}
function showHiddenInvoice(a) {
    if (jQuery("#needInvoice").attr("checked")) {
        invoceControl = true;
        jQuery("#newInvoiceDiv").css("display", "block")
    } else {
        invoceControl = false;
        jQuery.post("/checkout/confirm/canceledInvoice.do");
        jQuery("#newInvoiceDiv").css("display", "none")
    }
}
function showYaoWangDisplay(a) {
    if (jQuery("#needInvoice").attr("checked")) {
        jQuery("#yaowangDisplay").css("display", "inline-block")
    } else {
        jQuery("#yaowangDisplay").css("display", "none")
    }
}
function chooseOrdinary() {
    chooseInvoiceType = 2;
    jQuery(".zzs_fp").hide();
    jQuery(".normal_fp").show()
}
function chooseVTA() {
    chooseInvoiceType = 3;
    jQuery(".normal_fp").hide();
    jQuery(".zzs_fp").show()
}
function chooseHead(b) {
    var a = jQuery("#headType option:selected").val();
    if (a == "个人") {
        jQuery("#normal_head").hide()
    } else {
        jQuery("#normal_head").show()
    }
}
function clickNormalHead(b) {
    var a = jQuery(b).val();
    if (a == "单位名称") {
        jQuery(b).val("")
    }
}
function enableNext() {
    jQuery("#next").attr("disabled", false)
}
function checkUserPoint() {
    jQuery.post("/checkout/confirm/checkUserPoint.do?", "", afterCheckUserPoint)
}
function afterCheckUserPoint(a) {
    checkStock()
}
function checkPoints() {
    var a = parseFloat(jQuery("#needPoints").html());
    a = a.toFixed(2);
    jQuery("#next").attr("disabled", true);
    jQuery.post("/pingan/queryPointsAmount.do?rd=" + Math.random(), "", popPoints)
}
function popPoints(e) {
    if (!redirectIfNotLogin(e)) {
        return false
    }
    var b = parseFloat(jQuery("#needPoints").html());
    var j = e;
    var i = -1;
    if (j) {
        var d = j.split("=");
        if (d.length > 0) {
            var l = d[0];
            if (l == 1) {
                var a = d[1];
                var h = a.split(",");
                i = h[0];
                var g = h[1];
                var c = document.getElementById("wltPoints");
                if (c) {
                    c.innerHTML = i;
                    jQuery("#wltPoints").css("display", "");
                    jQuery("#wltPoints_waiting").css("display", "none")
                }
                var f = document.getElementById("wltPoints2");
                if (f) {
                    f.innerHTML = i;
                    jQuery("#wltPoints2").css("display", "");
                    jQuery("#wltPoints2_waiting").css("display", "none")
                }
            }
        }
    }
    var k = jQuery("#paymentListDiv") && jQuery("#paymentListDiv").css("display") != "none";
    if (i == -1 && k) {
        jQuery("#next").attr("disabled", true);
        alert("无法获取您的万里通积分信息，请稍后再试。");
        return
    }
    if (b > i && k) {
        jQuery("#next").attr("disabled", true);
        alert("您的万里通积分不足,当前您的万里通积分为:" + i)
    } else {
        jQuery("#next").attr("disabled", false)
    }
}
function getOrderProducts() {
    jQuery.post("/checkout/confirm/getOrderProducts.do?rd=" + Math.random(), "", afterGetOrderProducts)
}
function afterGetOrderProducts(a) {
    if (!redirectIfNotLogin(a)) {
        return false
    }
    jQuery("#productListDiv").html(a);
    clearWaitInfo()
}
function waitForSubmitOrder() {
    jQuery("body").block({
        message: '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="73%" height="50" align="center" class="font14"><img src="http://image.yihaodian.com/images/wait_loading.gif"/></td></tr><tr><td height="25" align="center" class="font14">您的订单正在处理中,请稍候...</td></tr></table>',
        css: {
            padding: 0,
            margin: 0,
            width: "25%",
            height: "10%",
            border: "5px solid #FFCC00",
            opacity: 0.9,
            backgroundColor: "#FEFFDF"
        },
        overlayCSS: {
            backgroundColor: "#000",
            opacity: 0.1,
            cursor: "default"
        }
    })
}
function unWaitForSubmitOrder() {
    jQuery("body").unblock()
};
function showDetail(b, c) {
    if (!b) {
        return
    }
    var a = c.clientX + document.documentElement.scrollLeft;
    var d = c.clientY + document.documentElement.scrollTop;
    document.getElementById("div" + b).style.top = (d - 5) + "px";
    document.getElementById("div" + b).style.left = (a - 5) + "px";
    document.getElementById("div" + b).style.display = "block"
}
function closeIt(a) {
    if (!a) {
        return
    }
    jQuery("#detail" + a).css("display", "none")
}
function initMenu(a) {
    ul = jQuery("#detail" + a);
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        li[i].onmouseover = function() {
            try {
                jQuery("#div" + a).css("display", "block")
            } catch(b) {}
        };
        li[i].onmouseout = function() {
            try {
                jQuery("#div" + a).css("display", "none")
            } catch(b) {}
        }
    }
}
function clearType(c, a, b) {
    jQuery("input[id*=type" + c + "coupon]:checked,input[id*=type" + a + "coupon]:checked,input[id*=type" + b + "coupon]:checked").each(function() {
        jQuery(this).attr("checked", false)
    })
}
function checkCoupon() {
    var a = "";
    if (jQuery("#addCouponNumber").size() > 0) {
        a = jQuery.trim(jQuery("#addCouponNumber").val())
    } else {
        a = jQuery.trim(jQuery("#couponNumber").val())
    }
    if (!a || a == "") {
        jQuery("#couponAmount").html("0");
        jQuery("#coupon_desc").html("");
        return
    }
    jQuery.post("/product/checkCoupon.do", {
        "coupon.number": a
    },
    updateCoupon)
}
function updateCoupon(d) {
    if (!redirectIfNotLogin(d)) {
        return false
    }
    var e = d;
    if (e != "") {
        var c = e.split("=");
        var a = c[0];
        var f = c[1];
        if (a == "0") {
            jQuery("#errorArea").html("");
            jQuery("#couponAmount").html(f)
        } else {
            jQuery("#errorArea").html(e);
            jQuery("#couponAmount").html("0")
        }
    }
    if (jQuery("#errorArea").html() != "") {
        return
    }
    var b = "";
    if (jQuery("#addCouponNumber").size() > 0) {
        b = jQuery.trim(jQuery("#addCouponNumber").val())
    } else {
        b = jQuery.trim(jQuery("#couponNumber").val())
    }
    if (b.trim() != "") {
        jQuery.post("/product/addCoupon.do", {
            couponNumber: b
        },
        showCouponInfo)
    } else {
        alert("\u8bf7\u8f93\u5165\u62b5\u7528\u5238\u53f7\u7801");
        return
    }
}
function removeCoupons() {
    jQuery.post("/product/removeCoupon.do", "", showCouponInfo)
}
function showCouponInfo(b) {
    if (!redirectIfNotLogin(b)) {
        return false
    }
    var a = b;
    if (a) {
        var c = a.split("==");
        if (c[0] == "0") {
            doGetAmountList();
            jQuery("#errorArea").html("");
            jQuery("#couponArea").html(c[1])
        } else {
            jQuery("#errorArea").html(c[1])
        }
    }
}
function addCoupon() {
    checkCoupon()
}
function addCouponsConfirm() {
    var a = "";
    jQuery("input[id*=coupon]:checked").each(function() {
        a = a + jQuery(this).val() + ","
    });
    jQuery.post("/product/addCoupon.do", {
        couponNumber: a
    },
    showCouponInfo)
}
function addCoupons() {
    var a = "";
    jQuery("input[id*=coupon]:checked").each(function() {
        a = a + jQuery(this).val() + ","
    });
    if (a == "") {
        a = jQuery("#couponNumber").val()
    }
    jQuery.post("/product/addCoupon.do", {
        couponNumber: a
    },
    showCouponInfo)
}
function couponsDefVal(a) {
    if (a.value == "\u8f93\u5165\u60a8\u7684\u62b5\u7528\u5238\u7f16\u7801") {
        a.value = "";
        jQuery("#couponNumber").css("color", "black")
    }
}
function showFloatTheseProduct(a) {
    clearTimeout(floatTheseProductTimeout);
    jQuery("div[id^='ap_titlebox_']").not("#ap_titlebox_" + a).hide();
    jQuery("#titlemenu_" + a).removeClass();
    jQuery("#titlemenu_" + a).addClass("ap_titlebox_menu_off");
    jQuery("#ap_titlebox_" + a).show();
    if (jQuery(window).width() - jQuery("#titlemenu_" + a).offset().left < 472) {
        jQuery("#ap_titlebox_" + a).css("left", jQuery("#titlemenu_" + a).offset().left - 397 + "px");
        jQuery("#ap_titlebox_" + a).css("top", jQuery("#titlemenu_" + a).offset().top + 24 + "px")
    } else {
        jQuery("#ap_titlebox_" + a).css("left", jQuery("#titlemenu_" + a).offset().left + "px");
        jQuery("#ap_titlebox_" + a).css("top", jQuery("#titlemenu_" + a).offset().top + 24 + "px")
    }
}
function hideFloatTheseProduct(a) {
    floatTheseProductTimeout = setTimeout("jQuery('#ap_titlebox_" + a + "').hide()", 100);
    jQuery("#titlemenu_" + a).removeClass();
    jQuery("#titlemenu_" + a).addClass("ap_titlebox_menu_on")
}
function check_mobile() {
    var a = document.getElementById("verifyMobile").value;
    if (a == "") {
        alert("请输入手机号码!");
        return false
    }
    var b = /^(1)\d{10}$/;
    if (!b.test(a)) {
        alert("手机号码不正确!");
        return false
    }
    return true
}
function doSendMobile() {
    if (!check_mobile()) {
        document.getElementById("verifyMobile").focus();
        return false
    }
    jQuery.post("/SMSVali/SMSSendValidateCode.do", {
        cellphone: document.getElementById("verifyMobile").value
    },
    sendMobileReturn);
    return true
}
function sendMobileReturn(a) {
    ret = a;
    if (ret == "success") {
        alert("验证码已成功发送到您的手机，请注意查收!")
    } else {
        if (ret == "validateCode is error") {
            alert("校验码输入错误!")
        } else {
            if (ret == "cellphone number is null") {
                alert("请输入手机号码!")
            } else {
                if (ret == "9") {
                    alert("您不能验证!")
                } else {
                    if (ret == "already valid") {
                        alert("您已通过验证，无需再验证！")
                    } else {
                        if (ret == "phonenum is exists") {
                            alert("该手机号已经和其他账户绑定，无法再次和您的账号绑定。")
                        } else {
                            if (ret == "too fast") {
                                alert("请稍后!每次发送间隔不能小于一分钟")
                            } else {
                                if (ret == "overflow times") {
                                    alert("您今天已验证5次，无法再验证。!")
                                } else {
                                    return
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
function doValidMobile() {
    if (!check_mobile()) {
        document.getElementById("verifyMobile").focus();
        return false
    }
    jQuery.post("/SMSVali/mobileValidate.do", {
        cellphone: document.getElementById("verifyMobile").value,
        smsValidateCode: document.getElementById("verifyMobileCode").value
    },
    validMobileReturn);
    return true
}
function validMobileReturn(a) {
    ret = a;
    if (ret == "success validate") {
        alert("验证成功!恭喜您!");
        addCoupons()
    } else {
        if (ret == "incorrect code") {
            alert("验证码错误!")
        } else {
            if (ret == "validateCode is null") {
                alert("验证码不能为空")
            } else {
                if (ret == "incorrect userId") {
                    alert("验证码无效")
                } else {
                    if (ret == "validate code is expired") {
                        alert("验证码已经过期")
                    } else {
                        if (ret == "cellphone number is null") {
                            alert("请输入手机号码!")
                        } else {
                            if (ret == "user is null") {
                                alert("您不能验证!")
                            } else {
                                if (ret == "already valid") {
                                    alert("您已通过验证！")
                                } else {
                                    if (ret == "phonenum is exists") {
                                        alert("该手机号码已被别人验证过,您不能使用!")
                                    } else {
                                        if (ret == "overflow times") {
                                            alert("您今天已验证5次，无法再验证!")
                                        } else {
                                            if (ret == "wrong times") {
                                                alert("验证码已失效，请重新获取验证码!")
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
};
/*
 * jQuery blockUI plugin
 * Version 2.33 (29-MAR-2010)
 * @requires jQuery v1.2.3 or later
 *
 * Examples at: http://malsup.com/jquery/block/
 * Copyright (c) 2007-2008 M. Alsup
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * Thanks to Amir-Hossein Sobhi for some excellent contributions!
 */
(function(i) {
    if (/1\.(0|1|2)\.(0|1|2)/.test(i.fn.jquery) || /^1.1/.test(i.fn.jquery)) {
        alert("blockUI requires jQuery v1.2.3 or later!  You are using v" + i.fn.jquery);
        return
    }
    i.fn._fadeIn = i.fn.fadeIn;
    var c = function() {};
    var j = document.documentMode || 0;
    var e = i.browser.msie && ((i.browser.version < 8 && !j) || j < 8);
    var f = i.browser.msie && /MSIE 6.0/.test(navigator.userAgent) && !j;
    i.blockUI = function(p) {
        d(window, p)
    };
    i.unblockUI = function(p) {
        h(window, p)
    };
    i.growlUI = function(t, r, s, p) {
        var q = i('<div class="growlUI"></div>');
        if (t) {
            q.append("<h1>" + t + "</h1>")
        }
        if (r) {
            q.append("<h2>" + r + "</h2>")
        }
        if (s == undefined) {
            s = 3000
        }
        i.blockUI({
            message: q,
            fadeIn: 700,
            fadeOut: 1000,
            centerY: false,
            timeout: s,
            showOverlay: false,
            onUnblock: p,
            css: i.blockUI.defaults.growlCSS
        })
    };
    i.fn.block = function(p) {
        return this.unblock({
            fadeOut: 0
        }).each(function() {
            if (i.css(this, "position") == "static") {
                this.style.position = "relative"
            }
            if (i.browser.msie) {
                this.style.zoom = 1
            }
            d(this, p)
        })
    };
    i.fn.unblock = function(p) {
        return this.each(function() {
            h(this, p)
        })
    };
    i.blockUI.version = 2.33;
    i.blockUI.defaults = {
        message: "<h1>Please wait...</h1>",
        title: null,
        draggable: true,
        theme: false,
        css: {
            padding: 0,
            margin: 0,
            width: "30%",
            top: "40%",
            left: "35%",
            textAlign: "center",
            color: "#000",
            border: "3px solid #aaa",
            backgroundColor: "#fff",
            cursor: "wait"
        },
        themedCSS: {
            width: "30%",
            top: "40%",
            left: "35%"
        },
        overlayCSS: {
            backgroundColor: "#000",
            opacity: 0.6,
            cursor: "wait"
        },
        growlCSS: {
            width: "350px",
            top: "10px",
            left: "",
            right: "10px",
            border: "none",
            padding: "5px",
            opacity: 0.6,
            cursor: "default",
            color: "#fff",
            backgroundColor: "#000",
            "-webkit-border-radius": "10px",
            "-moz-border-radius": "10px",
            "border-radius": "10px"
        },
        iframeSrc: /^https/i.test(window.location.href || "") ? "javascript:false": "about:blank",
        forceIframe: false,
        baseZ: 1000,
        centerX: true,
        centerY: true,
        allowBodyStretch: true,
        bindEvents: true,
        constrainTabKey: true,
        fadeIn: 200,
        fadeOut: 400,
        timeout: 0,
        showOverlay: true,
        focusInput: true,
        applyPlatformOpacityRules: true,
        onBlock: null,
        onUnblock: null,
        quirksmodeOffsetHack: 4
    };
    var b = null;
    var g = [];
    function d(r, F) {
        var A = (r == window);
        var w = F && F.message !== undefined ? F.message: undefined;
        F = i.extend({},
        i.blockUI.defaults, F || {});
        F.overlayCSS = i.extend({},
        i.blockUI.defaults.overlayCSS, F.overlayCSS || {});
        var C = i.extend({},
        i.blockUI.defaults.css, F.css || {});
        var N = i.extend({},
        i.blockUI.defaults.themedCSS, F.themedCSS || {});
        w = w === undefined ? F.message: w;
        if (A && b) {
            h(window, {
                fadeOut: 0
            })
        }
        if (w && typeof w != "string" && (w.parentNode || w.jquery)) {
            var I = w.jquery ? w[0] : w;
            var P = {};
            i(r).data("blockUI.history", P);
            P.el = I;
            P.parent = I.parentNode;
            P.display = I.style.display;
            P.position = I.style.position;
            if (P.parent) {
                P.parent.removeChild(I)
            }
        }
        var B = F.baseZ;
        var M = (i.browser.msie || F.forceIframe) ? i('<iframe class="blockUI" style="z-index:' + (B++) + ';display:none;border:none;margin:0;padding:0;position:absolute;width:100%;height:100%;top:0;left:0" src="' + F.iframeSrc + '"></iframe>') : i('<div class="blockUI" style="display:none"></div>');
        var L = i('<div class="blockUI blockOverlay" style="z-index:' + (B++) + ';display:none;border:none;margin:0;padding:0;width:100%;height:100%;top:0;left:0"></div>');
        var K, G;
        if (F.theme && A) {
            G = '<div class="blockUI blockMsg blockPage ui-dialog ui-widget ui-corner-all" style="z-index:' + B + ';display:none;position:fixed"><div class="ui-widget-header ui-dialog-titlebar blockTitle">' + (F.title || "&nbsp;") + '</div><div class="ui-widget-content ui-dialog-content"></div></div>'
        } else {
            if (F.theme) {
                G = '<div class="blockUI blockMsg blockElement ui-dialog ui-widget ui-corner-all" style="z-index:' + B + ';display:none;position:absolute"><div class="ui-widget-header ui-dialog-titlebar blockTitle">' + (F.title || "&nbsp;") + '</div><div class="ui-widget-content ui-dialog-content"></div></div>'
            } else {
                if (A) {
                    G = '<div class="blockUI blockMsg blockPage" style="z-index:' + B + ';display:none;position:fixed"></div>'
                } else {
                    G = '<div class="blockUI blockMsg blockElement" style="z-index:' + B + ';display:none;position:absolute"></div>'
                }
            }
        }
        K = i(G);
        if (w) {
            if (F.theme) {
                K.css(N);
                K.addClass("ui-widget-content")
            } else {
                K.css(C)
            }
        }
        if (!F.applyPlatformOpacityRules || !(i.browser.mozilla && /Linux/.test(navigator.platform))) {
            L.css(F.overlayCSS)
        }
        L.css("position", A ? "fixed": "absolute");
        if (i.browser.msie || F.forceIframe) {
            M.css("opacity", 0)
        }
        var y = [M, L, K],
        O = A ? i("body") : i(r);
        i.each(y,
        function() {
            this.appendTo(O)
        });
        if (F.theme && F.draggable && i.fn.draggable) {
            K.draggable({
                handle: ".ui-dialog-titlebar",
                cancel: "li"
            })
        }
        var v = e && (!i.boxModel || i("object,embed", A ? null: r).length > 0);
        if (f || v) {
            if (A && F.allowBodyStretch && i.boxModel) {
                i("html,body").css("height", "100%")
            }
            if ((f || !i.boxModel) && !A) {
                var E = m(r, "borderTopWidth"),
                J = m(r, "borderLeftWidth");
                var x = E ? "(0 - " + E + ")": 0;
                var D = J ? "(0 - " + J + ")": 0
            }
            i.each([M, L, K],
            function(t, S) {
                var z = S[0].style;
                z.position = "absolute";
                if (t < 2) {
                    A ? z.setExpression("height", "Math.max(document.body.scrollHeight, document.body.offsetHeight) - (jQuery.boxModel?0:" + F.quirksmodeOffsetHack + ') + "px"') : z.setExpression("height", 'this.parentNode.offsetHeight + "px"');
                    A ? z.setExpression("width", 'jQuery.boxModel && document.documentElement.clientWidth || document.body.clientWidth + "px"') : z.setExpression("width", 'this.parentNode.offsetWidth + "px"');
                    if (D) {
                        z.setExpression("left", D)
                    }
                    if (x) {
                        z.setExpression("top", x)
                    }
                } else {
                    if (F.centerY) {
                        if (A) {
                            z.setExpression("top", '(document.documentElement.clientHeight || document.body.clientHeight) / 2 - (this.offsetHeight / 2) + (blah = document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + "px"')
                        }
                        z.marginTop = 0
                    } else {
                        if (!F.centerY && A) {
                            var Q = (F.css && F.css.top) ? parseInt(F.css.top) : 0;
                            var R = "((document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + " + Q + ') + "px"';
                            z.setExpression("top", R)
                        }
                    }
                }
            })
        }
        if (w) {
            if (F.theme) {
                K.find(".ui-widget-content").append(w)
            } else {
                K.append(w)
            }
            if (w.jquery || w.nodeType) {
                i(w).show()
            }
        }
        if ((i.browser.msie || F.forceIframe) && F.showOverlay) {
            M.show()
        }
        if (F.fadeIn) {
            var H = F.onBlock ? F.onBlock: c;
            var q = (F.showOverlay && !w) ? H: c;
            var p = w ? H: c;
            if (F.showOverlay) {
                L._fadeIn(F.fadeIn, q)
            }
            if (w) {
                K._fadeIn(F.fadeIn, p)
            }
        } else {
            if (F.showOverlay) {
                L.show()
            }
            if (w) {
                K.show()
            }
            if (F.onBlock) {
                F.onBlock()
            }
        }
        l(1, r, F);
        if (A) {
            b = K[0];
            g = i(":input:enabled:visible", b);
            if (F.focusInput) {
                setTimeout(o, 20)
            }
        } else {
            a(K[0], F.centerX, F.centerY)
        }
        if (F.timeout) {
            var u = setTimeout(function() {
                A ? i.unblockUI(F) : i(r).unblock(F)
            },
            F.timeout);
            i(r).data("blockUI.timeout", u)
        }
    }
    function h(s, t) {
        var r = (s == window);
        var q = i(s);
        var u = q.data("blockUI.history");
        var v = q.data("blockUI.timeout");
        if (v) {
            clearTimeout(v);
            q.removeData("blockUI.timeout")
        }
        t = i.extend({},
        i.blockUI.defaults, t || {});
        l(0, s, t);
        var p;
        if (r) {
            p = i("body").children().filter(".blockUI").add("body > .blockUI")
        } else {
            p = i(".blockUI", s)
        }
        if (r) {
            b = g = null
        }
        if (t.fadeOut) {
            p.fadeOut(t.fadeOut);
            setTimeout(function() {
                k(p, u, t, s)
            },
            t.fadeOut)
        } else {
            k(p, u, t, s)
        }
    }
    function k(p, s, r, q) {
        p.each(function(t, u) {
            if (this.parentNode) {
                this.parentNode.removeChild(this)
            }
        });
        if (s && s.el) {
            s.el.style.display = s.display;
            s.el.style.position = s.position;
            if (s.parent) {
                s.parent.appendChild(s.el)
            }
            i(q).removeData("blockUI.history")
        }
        if (typeof r.onUnblock == "function") {
            r.onUnblock(q, r)
        }
    }
    function l(p, t, u) {
        var s = t == window,
        r = i(t);
        if (!p && (s && !b || !s && !r.data("blockUI.isBlocked"))) {
            return
        }
        if (!s) {
            r.data("blockUI.isBlocked", p)
        }
        if (!u.bindEvents || (p && !u.showOverlay)) {
            return
        }
        var q = "mousedown mouseup keydown keypress";
        p ? i(document).bind(q, u, n) : i(document).unbind(q, n)
    }
    function n(s) {
        if (s.keyCode && s.keyCode == 9) {
            if (b && s.data.constrainTabKey) {
                var r = g;
                var q = !s.shiftKey && s.target == r[r.length - 1];
                var p = s.shiftKey && s.target == r[0];
                if (q || p) {
                    setTimeout(function() {
                        o(p)
                    },
                    10);
                    return false
                }
            }
        }
        if (i(s.target).parents("div.blockMsg").length > 0) {
            return true
        }
        return i(s.target).parents().children().filter("div.blockUI").length == 0
    }
    function o(p) {
        if (!g) {
            return
        }
        var q = g[p === true ? g.length - 1 : 0];
        if (q) {
            q.focus()
        }
    }
    function a(w, q, A) {
        var z = w.parentNode,
        v = w.style;
        var r = ((z.offsetWidth - w.offsetWidth) / 2) - m(z, "borderLeftWidth");
        var u = ((z.offsetHeight - w.offsetHeight) / 2) - m(z, "borderTopWidth");
        if (q) {
            v.left = r > 0 ? (r + "px") : "0"
        }
        if (A) {
            v.top = u > 0 ? (u + "px") : "0"
        }
    }
    function m(q, r) {
        return parseInt(i.css(q, r)) || 0
    }
})(jQuery);
Date.dayNames = ["日", "一", "二", "三", "四", "五", "六"];
Date.abbrDayNames = ["日", "一", "二", "三", "四", "五", "六"];
Date.monthNames = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"];
Date.abbrMonthNames = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"];
Date.firstDayOfWeek = 0;
Date.format = "yyyy-mm-dd";
Date.fullYearStart = "20"; (function() {
    function b(c, d) {
        if (!Date.prototype[c]) {
            Date.prototype[c] = d
        }
    }
    b("isLeapYear",
    function() {
        var c = this.getFullYear();
        return (c % 4 == 0 && c % 100 != 0) || c % 400 == 0
    });
    b("isWeekend",
    function() {
        return this.getDay() == 0 || this.getDay() == 6
    });
    b("isWeekDay",
    function() {
        return ! this.isWeekend()
    });
    b("getDaysInMonth",
    function() {
        return [31, (this.isLeapYear() ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][this.getMonth()]
    });
    b("getDayName",
    function(c) {
        return c ? Date.abbrDayNames[this.getDay()] : Date.dayNames[this.getDay()]
    });
    b("getMonthName",
    function(c) {
        return c ? Date.abbrMonthNames[this.getMonth()] : Date.monthNames[this.getMonth()]
    });
    b("getDayOfYear",
    function() {
        var c = new Date("1/1/" + this.getFullYear());
        return Math.floor((this.getTime() - c.getTime()) / 86400000)
    });
    b("getWeekOfYear",
    function() {
        return Math.ceil(this.getDayOfYear() / 7)
    });
    b("setDayOfYear",
    function(c) {
        this.setMonth(0);
        this.setDate(c);
        return this
    });
    b("addYears",
    function(c) {
        this.setFullYear(this.getFullYear() + c);
        return this
    });
    b("addMonths",
    function(d) {
        var c = this.getDate();
        this.setMonth(this.getMonth() + d);
        if (c > this.getDate()) {
            this.addDays( - this.getDate())
        }
        return this
    });
    b("addDays",
    function(c) {
        this.setTime(this.getTime() + (c * 86400000));
        return this
    });
    b("addHours",
    function(c) {
        this.setHours(this.getHours() + c);
        return this
    });
    b("addMinutes",
    function(c) {
        this.setMinutes(this.getMinutes() + c);
        return this
    });
    b("addSeconds",
    function(c) {
        this.setSeconds(this.getSeconds() + c);
        return this
    });
    b("zeroTime",
    function() {
        this.setMilliseconds(0);
        this.setSeconds(0);
        this.setMinutes(0);
        this.setHours(0);
        return this
    });
    b("asString",
    function(d) {
        var c = d || Date.format;
        if (c.split("mm").length > 1) {
            c = c.split("mmmm").join(this.getMonthName(false)).split("mmm").join(this.getMonthName(true)).split("mm").join(a(this.getMonth() + 1))
        } else {
            c = c.split("m").join(this.getMonth() + 1)
        }
        c = c.split("yyyy").join(this.getFullYear()).split("yy").join((this.getFullYear() + "").substring(2)).split("dd").join(a(this.getDate())).split("d").join(this.getDate());
        return c
    });
    Date.fromString = function(h) {
        var e = Date.format;
        var l = new Date("01/01/1970");
        if (h == "") {
            return l
        }
        h = h.toLowerCase();
        var d = "";
        var n = [];
        var k = /(dd?d?|mm?m?|yy?yy?)+([^(m|d|y)])?/g;
        var q;
        while ((q = k.exec(e)) != null) {
            switch (q[1]) {
            case "d":
            case "dd":
            case "m":
            case "mm":
            case "yy":
            case "yyyy":
                d += "(\\d+\\d?\\d?\\d?)+";
                n.push(q[1].substr(0, 1));
                break;
            case "mmm":
                d += "([a-z]{3})";
                n.push("M");
                break
            }
            if (q[2]) {
                d += q[2]
            }
        }
        var c = new RegExp(d);
        var m = h.match(c);
        if (m != null) {
            for (var p = 0; p < n.length; p++) {
                var g = m[p + 1];
                switch (n[p]) {
                case "d":
                    l.setDate(g);
                    break;
                case "m":
                    l.setMonth(Number(g) - 1);
                    break;
                case "M":
                    for (var o = 0; o < Date.abbrMonthNames.length; o++) {
                        if (Date.abbrMonthNames[o].toLowerCase() == g) {
                            break
                        }
                    }
                    l.setMonth(o);
                    break;
                case "y":
                    l.setYear(g);
                    break
                }
            }
        }
        return l
    };
    var a = function(c) {
        var d = "0" + c;
        return d.substring(d.length - 2)
    }
})(); (function(b) {
    b.fn.extend({
        renderCalendar: function(x) {
            var p = function(i) {
                return document.createElement(i)
            };
            x = b.extend({},
            b.fn.datePicker.defaults, x);
            if (x.showHeader != b.dpConst.SHOW_HEADER_NONE) {
                var o = b(p("tr"));
                for (var A = Date.firstDayOfWeek; A < Date.firstDayOfWeek + 7; A++) {
                    var h = A % 7;
                    var z = Date.dayNames[h];
                    o.append(jQuery(p("th")).attr({
                        scope: "col",
                        abbr: z,
                        title: z,
                        "class": (h == 0 || h == 6 ? "weekend": "weekday")
                    }).html(x.showHeader == b.dpConst.SHOW_HEADER_SHORT ? z.substr(0, 1) : z))
                }
            }
            var e = b(p("table")).attr({
                cellspacing: 0,
                cellpadding: 0
            }).addClass("jCalendar").append((x.showHeader != b.dpConst.SHOW_HEADER_NONE ? b(p("thead")).append(o) : p("thead")));
            var f = b(p("tbody"));
            var C = (new Date()).zeroTime();
            var v = x.month == undefined ? C.getMonth() : x.month;
            var q = x.year || C.getFullYear();
            var m = new Date(q, v, 1);
            var l = Date.firstDayOfWeek - m.getDay() + 1;
            if (l > 1) {
                l -= 7
            }
            var u = Math.ceil((( - 1 * l + 1) + m.getDaysInMonth()) / 7);
            m.addDays(l - 1);
            var t = function(i) {
                return function() {
                    if (x.hoverClass) {
                        var r = b(this);
                        if (!x.selectWeek) {
                            r.addClass(x.hoverClass)
                        } else {
                            if (i && !r.is(".disabled")) {
                                r.parent().addClass("activeWeekHover")
                            }
                        }
                    }
                }
            };
            var g = function() {
                if (x.hoverClass) {
                    var i = b(this);
                    i.removeClass(x.hoverClass);
                    i.parent().removeClass("activeWeekHover")
                }
            };
            var n = 0;
            while (n++<u) {
                var y = jQuery(p("tr"));
                var k = x.dpController ? m > x.dpController.startDate: false;
                for (var A = 0; A < 7; A++) {
                    var j = m.getMonth() == v;
                    var B = b(p("td")).text(m.getDate() + "").addClass((j ? "current-month ": "other-month ") + (m.isWeekend() ? "weekend ": "weekday ") + (j && m.getTime() == C.getTime() ? "today ": "")).data("datePickerDate", m.asString()).hover(t(k), g);
                    y.append(B);
                    if (x.renderCallback) {
                        x.renderCallback(B, m, v, q)
                    }
                    m = new Date(m.getFullYear(), m.getMonth(), m.getDate() + 1)
                }
                f.append(y)
            }
            e.append(f);
            return this.each(function() {
                b(this).empty().append(e)
            })
        },
        datePicker: function(e) {
            if (!b.event._dpCache) {
                b.event._dpCache = []
            }
            e = b.extend({},
            b.fn.datePicker.defaults, e);
            return this.each(function() {
                var h = b(this);
                var f = true;
                if (!this._dpId) {
                    this._dpId = b.event.guid++;
                    b.event._dpCache[this._dpId] = new c(this);
                    f = false
                }
                if (e.inline) {
                    e.createButton = false;
                    e.displayClose = false;
                    e.closeOnSelect = false;
                    h.empty()
                }
                var g = b.event._dpCache[this._dpId];
                g.init(e);
                if (!f && e.createButton) {
                    g.button = b('<a href="#" class="dp-choose-date" title="' + b.dpText.TEXT_CHOOSE_DATE + '">' + b.dpText.TEXT_CHOOSE_DATE + "</a>").bind("click",
                    function() {
                        h.dpDisplay(this);
                        this.blur();
                        return false
                    });
                    h.after(g.button)
                }
                if (!f && h.is(":text")) {
                    h.bind("dateSelected",
                    function(j, l, k) {
                        this.value = l.asString()
                    }).bind("change",
                    function() {
                        if (this.value == "") {
                            g.clearSelected()
                        } else {
                            var j = Date.fromString(this.value);
                            if (j) {
                                g.setSelected(j, true, true)
                            }
                        }
                    });
                    if (e.clickInput) {
                        h.bind("click",
                        function() {
                            h.trigger("change");
                            h.dpDisplay()
                        })
                    }
                    var i = Date.fromString(this.value);
                    if (this.value != "" && i) {
                        g.setSelected(i, true, true)
                    }
                }
                h.addClass("dp-applied")
            })
        },
        dpSetDisabled: function(e) {
            return d.call(this, "setDisabled", e)
        },
        dpSetDisabledDate: function(e) {
            return d.call(this, "setDisabledDate", e)
        },
        dpSetStartDate: function(e) {
            return d.call(this, "setStartDate", e)
        },
        dpSetEndDate: function(e) {
            return d.call(this, "setEndDate", e)
        },
        dpGetSelected: function() {
            var e = a(this[0]);
            if (e) {
                return e.getSelected()
            }
            return null
        },
        dpSetSelected: function(f, h, g, e) {
            if (h == undefined) {
                h = true
            }
            if (g == undefined) {
                g = true
            }
            if (e == undefined) {
                e = true
            }
            return d.call(this, "setSelected", Date.fromString(f), h, g, e)
        },
        dpSetDisplayedMonth: function(e, f) {
            return d.call(this, "setDisplayedMonth", Number(e), Number(f), true)
        },
        dpDisplay: function(e) {
            return d.call(this, "display", e)
        },
        dpSetRenderCallback: function(e) {
            return d.call(this, "setRenderCallback", e)
        },
        dpSetPosition: function(e, f) {
            return d.call(this, "setPosition", e, f)
        },
        dpSetOffset: function(e, f) {
            return d.call(this, "setOffset", e, f)
        },
        dpClose: function() {
            return d.call(this, "_closeCalendar", false, this[0])
        },
        _dpDestroy: function() {}
    });
    var d = function(i, h, g, f, e) {
        return this.each(function() {
            var j = a(this);
            if (j) {
                j[i](h, g, f, e)
            }
        })
    };
    function c(e) {
        this.ele = e;
        this.displayedMonth = null;
        this.displayedYear = null;
        this.startDate = null;
        this.endDate = null;
        this.disabledDate = null;
        this.showYearNavigation = null;
        this.closeOnSelect = null;
        this.displayClose = null;
        this.rememberViewedMonth = null;
        this.selectMultiple = null;
        this.numSelectable = null;
        this.numSelected = null;
        this.verticalPosition = null;
        this.horizontalPosition = null;
        this.verticalOffset = null;
        this.horizontalOffset = null;
        this.button = null;
        this.renderCallback = [];
        this.selectedDates = {};
        this.inline = null;
        this.context = "#dp-popup";
        this.settings = {}
    }
    b.extend(c.prototype, {
        init: function(e) {
            this.setDisabledDate(e.disabledDate);
            this.setStartDate(e.startDate);
            this.setEndDate(e.endDate);
            this.setDisplayedMonth(Number(e.month), Number(e.year));
            this.setRenderCallback(e.renderCallback);
            this.showYearNavigation = e.showYearNavigation;
            this.closeOnSelect = e.closeOnSelect;
            this.displayClose = e.displayClose;
            this.rememberViewedMonth = e.rememberViewedMonth;
            this.selectMultiple = e.selectMultiple;
            this.numSelectable = e.selectMultiple ? e.numSelectable: 1;
            this.numSelected = 0;
            this.verticalPosition = e.verticalPosition;
            this.horizontalPosition = e.horizontalPosition;
            this.hoverClass = e.hoverClass;
            this.setOffset(e.verticalOffset, e.horizontalOffset);
            this.inline = e.inline;
            this.settings = e;
            if (this.inline) {
                this.context = this.ele;
                this.display()
            }
        },
        setDisabledDate: function(e) {
            if (e) {
                this.disabledDate = e
            }
        },
        setStartDate: function(e) {
            if (e) {
                this.startDate = Date.fromString(e)
            }
            if (!this.startDate) {
                this.startDate = (new Date()).zeroTime()
            }
            this.setDisplayedMonth(this.displayedMonth, this.displayedYear)
        },
        setEndDate: function(e) {
            if (e) {
                this.endDate = Date.fromString(e)
            }
            if (!this.endDate) {
                this.endDate = (new Date("12/31/2999"))
            }
            if (this.endDate.getTime() < this.startDate.getTime()) {
                this.endDate = this.startDate
            }
            this.setDisplayedMonth(this.displayedMonth, this.displayedYear)
        },
        setPosition: function(e, f) {
            this.verticalPosition = e;
            this.horizontalPosition = f
        },
        setOffset: function(e, f) {
            this.verticalOffset = parseInt(e) || 0;
            this.horizontalOffset = parseInt(f) || 0
        },
        setDisabled: function(e) {
            $e = b(this.ele);
            $e[e ? "addClass": "removeClass"]("dp-disabled");
            if (this.button) {
                $but = b(this.button);
                $but[e ? "addClass": "removeClass"]("dp-disabled");
                $but.attr("title", e ? "": b.dpText.TEXT_CHOOSE_DATE)
            }
            if ($e.is(":text")) {
                $e.attr("disabled", e ? "disabled": "")
            }
        },
        setDisplayedMonth: function(i, h, l) {
            if (this.startDate == undefined || this.endDate == undefined) {
                return
            }
            var k = new Date(this.startDate.getTime());
            k.setDate(1);
            var g = new Date(this.endDate.getTime());
            g.setDate(1);
            var f;
            if ((!i && !h) || (isNaN(i) && isNaN(h))) {
                f = new Date().zeroTime();
                f.setDate(1)
            } else {
                if (isNaN(i)) {
                    f = new Date(h, this.displayedMonth, 1)
                } else {
                    if (isNaN(h)) {
                        f = new Date(this.displayedYear, i, 1)
                    } else {
                        f = new Date(h, i, 1)
                    }
                }
            }
            if (f.getTime() < k.getTime()) {
                f = k
            } else {
                if (f.getTime() > g.getTime()) {
                    f = g
                }
            }
            var j = this.displayedMonth;
            var e = this.displayedYear;
            this.displayedMonth = f.getMonth();
            this.displayedYear = f.getFullYear();
            if (l && (this.displayedMonth != j || this.displayedYear != e)) {
                this._rerenderCalendar();
                b(this.ele).trigger("dpMonthChanged", [this.displayedMonth, this.displayedYear])
            }
        },
        setSelected: function(g, h, j, f) {
            if (g < this.startDate || g > this.endDate) {
                return
            }
            var l = this.settings;
            if (l.selectWeek) {
                g = g.addDays( - (g.getDay() - Date.firstDayOfWeek + 7) % 7);
                if (g < this.startDate) {
                    return
                }
            }
            if (h == this.isSelected(g)) {
                return
            }
            if (this.selectMultiple == false) {
                this.clearSelected()
            } else {
                if (h && this.numSelected == this.numSelectable) {
                    return
                }
            }
            if (j && (this.displayedMonth != g.getMonth() || this.displayedYear != g.getFullYear())) {
                this.setDisplayedMonth(g.getMonth(), g.getFullYear(), true)
            }
            this.selectedDates[g.toString()] = h;
            this.numSelected += h ? 1 : -1;
            var k = "td." + (g.getMonth() == this.displayedMonth ? "current-month": "other-month");
            var e;
            b(k, this.context).each(function() {
                if (b(this).data("datePickerDate") == g.asString()) {
                    e = b(this);
                    if (l.selectWeek) {
                        e.parent()[h ? "addClass": "removeClass"]("selectedWeek")
                    }
                    e[h ? "addClass": "removeClass"]("selected")
                }
            });
            b("td", this.context).not(".selected")[this.selectMultiple && this.numSelected == this.numSelectable ? "addClass": "removeClass"]("unselectable");
            if (f) {
                var l = this.isSelected(g);
                $e = b(this.ele);
                var i = Date.fromString(g.asString());
                $e.trigger("dateSelected", [i, e, l]);
                $e.trigger("change")
            }
        },
        isSelected: function(e) {
            return this.selectedDates[e.toString()]
        },
        getSelected: function() {
            var e = [];
            for (s in this.selectedDates) {
                if (this.selectedDates[s] == true) {
                    e.push(Date.parse(s))
                }
            }
            return e
        },
        clearSelected: function() {
            this.selectedDates = {};
            this.numSelected = 0;
            b("td.selected", this.context).removeClass("selected").parent().removeClass("selectedWeek")
        },
        display: function(l) {
            if (b(this.ele).is(".dp-disabled")) {
                return
            }
            l = l || this.ele;
            var i = this;
            var e = b(l);
            var h = e.offset();
            var j;
            var k;
            var n;
            var f;
            if (i.inline) {
                j = b(this.ele);
                k = {
                    id: "calendar-" + this.ele._dpId,
                    "class": "dp-popup dp-popup-inline"
                };
                b(".dp-popup", j).remove();
                f = {}
            } else {
                j = b("body");
                k = {
                    id: "dp-popup",
                    "class": "dp-popup"
                };
                f = {
                    top: h.top + i.verticalOffset + 20,
                    left: h.left + i.horizontalOffset
                };
                var g = function(r) {
                    var p = r.target;
                    var q = b("#dp-popup")[0];
                    while (true) {
                        if (p == q) {
                            return true
                        } else {
                            if (p == document) {
                                i._closeCalendar();
                                return false
                            } else {
                                p = b(p).parent()[0]
                            }
                        }
                    }
                };
                this._checkMouse = g;
                i._closeCalendar(true);
                b(document).bind("keydown.datepicker",
                function(p) {
                    if (p.keyCode == 27) {
                        i._closeCalendar()
                    }
                })
            }
            if (!i.rememberViewedMonth) {
                var o = this.getSelected()[0];
                if (o) {
                    o = new Date(o);
                    this.setDisplayedMonth(o.getMonth(), o.getFullYear(), false)
                }
            }
            j.append(b("<div></div>").attr(k).css(f).append(b("<h2></h2>"), b('<div class="dp-nav-prev"></div>').append(b('<a class="dp-nav-prev-year" href="#" title="' + b.dpText.TEXT_PREV_YEAR + '">&laquo;</a>').bind("click",
            function() {
                return i._displayNewMonth.call(i, this, 0, -1)
            }), b('<a class="dp-nav-prev-month" href="#" title="' + b.dpText.TEXT_PREV_MONTH + '">&lt;</a>').bind("click",
            function() {
                return i._displayNewMonth.call(i, this, -1, 0)
            })), b('<div class="dp-nav-next"></div>').append(b('<a class="dp-nav-next-year" href="#" title="' + b.dpText.TEXT_NEXT_YEAR + '">&raquo;</a>').bind("click",
            function() {
                return i._displayNewMonth.call(i, this, 0, 1)
            }), b('<a class="dp-nav-next-month" href="#" title="' + b.dpText.TEXT_NEXT_MONTH + '">&gt;</a>').bind("click",
            function() {
                return i._displayNewMonth.call(i, this, 1, 0)
            })), b('<div class="dp-calendar"></div>')).bgIframe());
            var m = this.inline ? b(".dp-popup", this.context) : b("#dp-popup");
            if (this.showYearNavigation == false) {
                b(".dp-nav-prev-year, .dp-nav-next-year", i.context).css("display", "none")
            }
            if (this.displayClose) {
                m.append(b('<a href="#" id="dp-close">' + b.dpText.TEXT_CLOSE + "</a>").bind("click",
                function() {
                    i._closeCalendar();
                    return false
                }))
            }
            i._renderCalendar();
            b(this.ele).trigger("dpDisplayed", m);
            if (!i.inline) {
                if (this.verticalPosition == b.dpConst.POS_BOTTOM) {
                    m.css("top", h.top + e.height() - m.height() + i.verticalOffset)
                }
                if (this.horizontalPosition == b.dpConst.POS_RIGHT) {
                    m.css("left", h.left + e.width() - m.width() + i.horizontalOffset)
                }
                b(document).bind("mousedown.datepicker", this._checkMouse)
            }
        },
        setRenderCallback: function(e) {
            if (e == null) {
                return
            }
            if (e && typeof(e) == "function") {
                e = [e]
            }
            this.renderCallback = this.renderCallback.concat(e)
        },
        cellRender: function(e, g, i, h) {
            var f = this.dpController;
            var j = new Date(g.getTime());
            e.bind("click",
            function() {
                var k = b(this);
                if (!k.is(".disabled")) {
                    f.setSelected(j, !k.is(".selected") || !f.selectMultiple, false, true);
                    if (f.closeOnSelect) {
                        f._closeCalendar()
                    }
                    if (!b.browser.msie) {
                        b(f.ele).trigger("focus", [b.dpConst.DP_INTERNAL_FOCUS])
                    }
                }
            });
            if (f.isSelected(j)) {
                e.addClass("selected");
                if (f.settings.selectWeek) {
                    e.parent().addClass("selectedWeek")
                }
            } else {
                if (f.selectMultiple && f.numSelected == f.numSelectable) {
                    e.addClass("unselectable")
                }
            }
        },
        _applyRenderCallbacks: function() {
            var e = this;
            b("td", this.context).each(function() {
                for (var f = 0; f < e.renderCallback.length; f++) {
                    $td = b(this);
                    e.renderCallback[f].apply(this, [$td, Date.fromString($td.data("datePickerDate")), e.displayedMonth, e.displayedYear])
                }
            });
            return
        },
        _displayNewMonth: function(e, g, f) {
            if (!b(e).is(".disabled")) {
                this.setDisplayedMonth(this.displayedMonth + g, this.displayedYear + f, true)
            }
            e.blur();
            return false
        },
        _rerenderCalendar: function() {
            this._clearCalendar();
            this._renderCalendar()
        },
        _renderCalendar: function() {
            b("h2", this.context).html((new Date(this.displayedYear, this.displayedMonth, 1)).asString(b.dpText.HEADER_FORMAT));
            b(".dp-calendar", this.context).renderCalendar(b.extend({},
            this.settings, {
                month: this.displayedMonth,
                year: this.displayedYear,
                renderCallback: this.cellRender,
                dpController: this,
                hoverClass: this.hoverClass
            }));
            var h = this.disabledDate;
            var f = function(r, j) {
                var p = false;
                if (r != null && j != null) {
                    var q = r.split(",");
                    if (q.length > 0) {
                        for (var i = 0; i < q.length; i++) {
                            if (parseInt(j) == parseInt(q[i])) {
                                p = true;
                                break
                            }
                        }
                    }
                }
                return p
            };
            if (this.displayedYear == this.startDate.getFullYear() && this.displayedMonth == this.startDate.getMonth()) {
                b(".dp-nav-prev-year", this.context).addClass("disabled");
                b(".dp-nav-prev-month", this.context).addClass("disabled");
                b(".dp-calendar td.other-month", this.context).each(function() {
                    var i = b(this);
                    if (Number(i.text()) > 20) {
                        i.addClass("disabled")
                    }
                });
                var e = this.startDate.getDate();
                b(".dp-calendar td.current-month", this.context).each(function() {
                    var i = b(this);
                    if (Number(i.text()) < e) {
                        i.addClass("disabled")
                    }
                })
            } else {
                b(".dp-nav-prev-year", this.context).removeClass("disabled");
                b(".dp-nav-prev-month", this.context).removeClass("disabled");
                var e = this.startDate.getDate();
                if (e > 20) {
                    var k = this.startDate.getTime();
                    var l = new Date(k);
                    l.addMonths(1);
                    if (this.displayedYear == l.getFullYear() && this.displayedMonth == l.getMonth()) {
                        b(".dp-calendar td.other-month", this.context).each(function() {
                            var i = b(this);
                            if (Date.fromString(i.data("datePickerDate")).getTime() < k) {
                                i.addClass("disabled")
                            }
                        })
                    }
                }
            }
            if (this.displayedYear == this.endDate.getFullYear() && this.displayedMonth == this.endDate.getMonth()) {
                b(".dp-nav-next-year", this.context).addClass("disabled");
                b(".dp-nav-next-month", this.context).addClass("disabled");
                b(".dp-calendar td.other-month", this.context).each(function() {
                    var i = b(this);
                    if (Number(i.text()) < 14) {
                        i.addClass("disabled")
                    }
                });
                var e = this.endDate.getDate();
                b(".dp-calendar td.current-month", this.context).each(function() {
                    var i = b(this);
                    if (Number(i.text()) > e) {
                        i.addClass("disabled")
                    }
                })
            } else {
                b(".dp-nav-next-year", this.context).removeClass("disabled");
                b(".dp-nav-next-month", this.context).removeClass("disabled");
                var e = this.endDate.getDate();
                if (e < 13) {
                    var g = new Date(this.endDate.getTime());
                    g.addMonths( - 1);
                    if (this.displayedYear == g.getFullYear() && this.displayedMonth == g.getMonth()) {
                        b(".dp-calendar td.other-month", this.context).each(function() {
                            var i = b(this);
                            if (Number(i.text()) > e) {
                                i.addClass("disabled")
                            }
                        })
                    }
                }
            }
            b(".dp-calendar td.current-month,.dp-calendar td.other-month", this.context).each(function() {
                var i = b(this);
                if (f(h, i.text())) {
                    i.addClass("disabled")
                }
            });
            this._applyRenderCallbacks()
        },
        _closeCalendar: function(e, f) {
            if (!f || f == this.ele) {
                b(document).unbind("mousedown.datepicker");
                b(document).unbind("keydown.datepicker");
                this._clearCalendar();
                b("#dp-popup a").unbind();
                b("#dp-popup").empty().remove();
                if (!e) {
                    b(this.ele).trigger("dpClosed", [this.getSelected()])
                }
            }
        },
        _clearCalendar: function() {
            b(".dp-calendar td", this.context).unbind();
            b(".dp-calendar", this.context).empty()
        }
    });
    b.dpConst = {
        SHOW_HEADER_NONE: 0,
        SHOW_HEADER_SHORT: 1,
        SHOW_HEADER_LONG: 2,
        POS_TOP: 0,
        POS_BOTTOM: 1,
        POS_LEFT: 0,
        POS_RIGHT: 1,
        DP_INTERNAL_FOCUS: "dpInternalFocusTrigger"
    };
    b.dpText = {
        TEXT_PREV_YEAR: "上一年",
        TEXT_PREV_MONTH: "上个月",
        TEXT_NEXT_YEAR: "下一年",
        TEXT_NEXT_MONTH: "下个月",
        TEXT_CLOSE: "关闭",
        TEXT_CHOOSE_DATE: "选择日期",
        HEADER_FORMAT: "mmmm yyyy"
    };
    b.dpVersion = "$Id: jquery.datePicker.js 70 2009-04-05 19:25:15Z kelvin.luck $";
    b.fn.datePicker.defaults = {
        month: undefined,
        year: undefined,
        showHeader: b.dpConst.SHOW_HEADER_SHORT,
        startDate: undefined,
        endDate: undefined,
        inline: false,
        renderCallback: null,
        createButton: false,
        showYearNavigation: true,
        closeOnSelect: true,
        displayClose: false,
        selectMultiple: false,
        numSelectable: Number.MAX_VALUE,
        clickInput: true,
        rememberViewedMonth: true,
        selectWeek: false,
        verticalPosition: b.dpConst.POS_TOP,
        horizontalPosition: b.dpConst.POS_LEFT,
        verticalOffset: 0,
        horizontalOffset: 0,
        hoverClass: "dp-hover"
    };
    function a(e) {
        if (e._dpId) {
            return b.event._dpCache[e._dpId]
        }
        return false
    }
    if (b.fn.bgIframe == undefined) {
        b.fn.bgIframe = function() {
            return this
        }
    }
    b(window).bind("unload",
    function() {
        var f = b.event._dpCache || [];
        for (var e in f) {
            b(f[e].ele)._dpDestroy()
        }
    })
})(jQuery);
Date.prototype.Format = function(e) {
    var g = e;
    var f = ["日", "一", "二", "三", "四", "五", "六"];
    var h = this.getMonth() + 1;
    g = g.replace(/yyyy|YYYY/, this.getFullYear());
    g = g.replace(/yy|YY/, (this.getYear() % 100) > 9 ? (this.getYear() % 100).toString() : "0" + (this.getYear() % 100));
    g = g.replace(/MM/, h > 9 ? h.toString() : "0" + h);
    g = g.replace(/M/g, h);
    g = g.replace(/w|W/g, f[this.getDay()]);
    g = g.replace(/dd|DD/, this.getDate() > 9 ? this.getDate().toString() : "0" + this.getDate());
    g = g.replace(/d|D/g, this.getDate());
    g = g.replace(/hh|HH/, this.getHours() > 9 ? this.getHours().toString() : "0" + this.getHours());
    g = g.replace(/h|H/g, this.getHours());
    g = g.replace(/mm/, this.getMinutes() > 9 ? this.getMinutes().toString() : "0" + this.getMinutes());
    g = g.replace(/m/g, this.getMinutes());
    g = g.replace(/ss|SS/, this.getSeconds() > 9 ? this.getSeconds().toString() : "0" + this.getSeconds());
    g = g.replace(/s|S/g, this.getSeconds());
    return g
};
Date.prototype.DateAdd = function(d, e) {
    var f = this;
    if (d != null) {
        switch (d) {
        case "s":
            return new Date(Date.parse(f) + (1000 * e));
        case "n":
            return new Date(Date.parse(f) + (60000 * e));
        case "h":
            return new Date(Date.parse(f) + (3600000 * e));
        case "d":
            return new Date(Date.parse(f) + (86400000 * e));
        case "w":
            return new Date(Date.parse(f) + ((86400000 * 7) * e));
        case "q":
            return new Date(f.getFullYear(), (f.getMonth()) + e * 3, f.getDate(), f.getHours(), f.getMinutes(), f.getSeconds());
        case "m":
            return new Date(f.getFullYear(), (f.getMonth()) + e, f.getDate(), f.getHours(), f.getMinutes(), f.getSeconds());
        case "y":
            return new Date((f.getFullYear() + e), f.getMonth(), f.getDate(), f.getHours(), f.getMinutes(), f.getSeconds())
        }
    }
};