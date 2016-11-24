jQuery(document).ready(function (e) {

    $ = jQuery;


    /*返回顶部*/
    $(function () {
        $(window).scroll(function () {
            if (!$('body').hasClass('probably-mobile')) {
                var e = $("#left-slide-bar");
                if ($(this).scrollTop() > 50) {
                    $('a#scroll-top').fadeIn();
                    $(e).css({top: 100});
                } else {
                    $('a#scroll-top').fadeOut();
                    $(e).css({top: 426})
                }
            }
            else {
                $('a#scroll-top').fadeOut();
            }


        });

        $('a#scroll-top').on('click', function () {
            if (!$('body').hasClass('probably-mobile')) {
                $('html, body').animate({scrollTop: 0}, 'slow');
                return false;
            }
        });


    });

    /*城市下拉选择*/
    $(".city-select").on('click', function (evt) {
        evt.stopPropagation();
        var input = $(this).find('.str'),
            dropObj = $(this).find('.city-menu'),
            _this = $(this),
            closeBtn = dropObj.find(".closebtn");
        $(this).addClass("current");

        closeBtn.on('click', function (evt) {
            evt.stopPropagation();
            _this.removeClass("current");
        });

    });
    $("body").on('click', function () {
        $(".city-select").removeClass("current");
    });


    $("body").on('click', function () {
        $(".city-select").removeClass("current");
    });


    $(".map li a").click(function (evt) {
        $provice = $(this).attr('provice'),
            $name = $(this).attr('name'),
            //alert($provice);
            $(".provice").val($provice);
        $(".name").val($name);
        $('.citySelect p').html($name);
        evt.stopPropagation();
        $(".city-select").removeClass("current");
    })


    $('#btn-search').click(function () {
        var provice = $(".provice").val();
        var key = $("#areaInput").val();
        var name = $(".name").val();
        if ($.trim(provice) == "") {
            errmsg('请选择省份');
            return false;
        } else if ($.trim(key) == "") {
            errmsg('请输入企业名称或注册号！');
            return false;
        } else if ($.trim(key).length < 2) {
            errmsg('企业名称至少2个关键字');
            return false;
        } else {
            window.location.href = encodeURI(INDEX_URL + "search?provice=" + provice + "&key=" + key + "&name=" + name);
        }
    });

    $("#searchAllInfos").on("click", function () {
        alert(0);
        var index = $("#index").val()
        var url = ''
        if (index > 0) {
            url = getUrl(index)
        }

    })


    function getUrl(index) {
        var url = '';
        switch (index) {
            case 1:
                url = '';
                break;
            case 2:
                url = '';
                break;
            case 3:
                url = '';
                break;
            case 4:
                url = '';
                break;
            case 5:
                url = '';
                break;
            case 6:
                url = '';
                break;
        }
        return url;

    }


    /*返回顶部*/
    $(function () {
        $('body').delegate('#left-slide-bar a', 'click', function (e) {
            e.preventDefault();
            var hash = $(this).attr('href');
            var offset = $(hash).offset().top;
            //alert(offset);
            $("#left-slide-bar a").each(function () {
                $(this).removeClass('active');
            });
            $(this).addClass('active').siblings().removeClass('active');
            $('body,html').animate({scrollTop: offset - 100}, 300);
        })
    });


    /*	个人中心 */
    $(function () {
        var avatar_timer = null;
        $('.nav-user').hover(
            function (event) {

                clearTimeout(avatar_timer);

                $('.profile-box').show();

            }, function () {
                avatar_timer = setTimeout(function () {
                    $('.profile-box').hide();
                }, 500);
            });
    });


    /*微信登录*/
    $(function () {
        var avatar_timer = null;
        $('.cc_btn-weixin').hover(
            function (event) {

                clearTimeout(avatar_timer);

                $('.share-dropdown').show();

            }, function () {
                avatar_timer = setTimeout(function () {
                    $('.share-dropdown').hide();
                }, 500);
            });
    });

    //重新认证邮箱
    $(".email2").click(function () {
        //alert($(this).attr('companykey'));
        $.post(INDEX_URL + '/user_changeEmailAction2', function (rs) {
            if (rs.success) {
                sucdia({content: "重新发送邮件成功，请尽快认证您的邮箱"});
            } else {
                faldia({
                    content: rs.msg,
                });
            }
        }, 'json');
    });

    $('.btn-guest').click(function () {
        var content = $(".content").val();
        var email = $(".email").val();
        if ($.trim(content) == "") {
            $(".contentmsg").text('请输入内容！');
            return false;
        } else if ($.trim(email) == "") {
            $(".emailmsg").text('请输入邮箱');
            return false;
        } else if (!$(".email").val().match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)) {
            $(".emailmsg").text('邮箱格式不正确');
            return false;
        } else {
            $.ajax({
                type: 'POST',
                url: INDEX_URL + '/guestbook_addAction',
                data: 'content=' + content + '&email=' + email,
                success: function (result) {
                    var delay;
                    delay = function (ms, func) {
                        return setTimeout(func, ms);
                    };
                    toastr.options = {
                        positionClass: 'toast-bottom-left'
                    };
                    delay(100, function () {
                        if (result.success) {
                            return toastr.success('恭喜你，反馈成功！');
                        } else {
                            return toastr.success(result.msg);
                        }

                    });
                    setTimeout(location.reload(), 2000);
                }
            });
        }
    });


    //操作错误对话框
    errmsg = function (content) {
        var delay;
        delay = function (ms, func) {
            return setTimeout(func, ms);
        };
        toastr.options = {
            positionClass: 'toast-bottom-left'
        };
        delay(10, function () {
            return toastr.error(content);
        });
    }


    //操作失败对话框
    errmsg2 = function (content) {
        var provice = $("#provice").val();
        var unique = $("#unique").val();
        fn = function () {
            location.href = INDEX_URL + "/user_login?back=" + INDEX_URL + "/firm_" + provice + "_" + unique;
        };
        var options = {};
        if (typeof(content) == 'string') {
            options.content = content;
            options.fn = fn || function () {
                };
        } else {
            options = content;
        }
        options.content = options.content || '保存失败！';
        options.time = options.time || 2;
        options.fn = options.fn || function () {
            };
        var delay;
        delay = function (ms, func) {
            return setTimeout(func, ms);
        };
        toastr.options = {
            positionClass: 'toast-bottom-left'
        };
        delay(10, function () {
            return toastr.error(options.content);
        });
        setTimeout(options.fn, 2000);
    }


    eval(function (p, a, c, k, e, r) {
        e = function (c) {
            return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
        };
        if (!''.replace(/^/, String)) {
            while (c--)r[e(c)] = k[c] || e(c);
            k = [function (e) {
                return r[e]
            }];
            e = function () {
                return '\\w+'
            };
            c = 1
        }
        ;
        while (c--)if (k[c])p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
        return p
    }('$(5(){$(".1").4();$("#i").v(5(){$(".1").4();0 e=$(".9").8();0 f=$("#i").8();0 g=$.k(e+f);3($.j(e)==""){6 7}2 3($.j(f)==""){$(".1").4();6 7}2{$.w({x:\'A\',D:l+\'/m\',n:\'9=\'+e+\'&o=\'+f+\'&p=\'+g,q:5(a){3(a=="s"){$(".t-u").h("网络状态异常");6 7}2{0 b="";0 c=y.z(a);0 d=c.B;3(d){$(".1").C();0 b=r(e,d);$(".1").h(b)}2{$(".1").4()}}}})}})});', 40, 40, 'var|list|else|if|hide|function|return|false|val|provice||||||||html|areaInput|trim|md5|INDEX_URL|gongsi_getList|data|key|token|success|dealInfoToHTML|null|result|msg|keyup|ajax|type|JSON|parse|POST|Result|show|url'.split('|'), 0, {}))


    $(function () {
        $("#search-list").hide();
        $("#header-search-list").hide();
        $("#searchkey").on('input', function (e) {
            searchList(1);
        })
        $("#searchkey").bind('click', function (e) {
            searchList(1);
        })
        $("#headerKey").on('input', function (e) {
            searchList(2);
        })
        $("#headerKey").bind('click', function (e) {
            searchList(2);
        })

        document.onclick = function (e) {
            var e = e ? e : window.event;
            var tar = e.srcElement || e.target;
            if (tar.id != "searchkey") {
                $("#search-list").hide();
            }
        }
    });

//搜索
    function searchList() {
        if (arguments[0] == 1) {
            var list = $("#search-list");
            var key = $("#searchkey");
        } else {
            var list = $("#header-search-list");
            var key = $("#headerKey");
        }
        list.hide();
        var f = key.val();
        var type = $("#index").val();
        if ($.trim(f) == "") {
            return false
        } else {
            $.ajax({
                type: 'POST',
                url: INDEX_URL + '/gongsi_getList',
                data: 'key=' + f + "&type=" + type,
                success: function (a) {
                    if (a == "null") {
                        //$(".result-msg").html("网络状态异常");
                        return false
                    } else {
                        var b = "";
                        var c = JSON.parse(a);
                        var d = c;
                        if (d) {
                            list.show();
                            var b = dealInfoToHTML(e, d);
                            list.html(b)
                        } else {
                            list.hide()
                        }
                    }
                }
            })
        }
    }


    /** 搜索结果html**/
    function dealInfoToHTML(provice, companys) {
        var html = '';
        html = html + "<div class='list-group no-radius alt'>";
        for (var i = 0; i < companys.length; i++) {
            html = html + "<a class='list-group-item' href='" + INDEX_URL + "/firm_" + companys[i].KeyNo + ".shtml'><span class='badge bg-info'>" + companys[i].Reason + "</span>" + companys[i].Name + "</a>";
        }
        html = html + "</div>";
        return html;
    }
});


//回复评论
function reply(e, u) {
    box = document.getElementById('comm');
    to = document.getElementById('to');
    to.value = u;
    //alert(u);
    oc = box.value;
    prefix = '@' + e + ' ';
    nc = oc + prefix;
    box.focus();
    box.value = nc;
}


$(function () {
    /**微信二维码扫描**/
    $("#wechat_code").hover(function () {
        //alert(123);
        $(".wechat_showplace").stop(true).show().animate({"top": "35px", "opacity": "1"});
    }, function () {
        $(".wechat_showplace").stop(true).animate({"top": "35px", "opacity": "0"}, 200, function () {
            $(this).hide();
        });
    });


    /**首页点击搜索**/


    $('.search-type').click(function () {
        $(".newlist").hide();
        $('.search-type').removeClass("active");
        $(this).addClass("active");
        //alert();
        var index = $(this).index();
        $("#index").val(index);
    });


    $(".fa-weixin").hover(function () {
            var screen_width = $(window).width()
            var container_width = $('.container').width()
            var num = (screen_width - container_width) / 2
            $("#chat").show()
            $("#chat").css("right", (num - 70) + 'px')
        },
        function () {
            $("#chat").hide();
        });


    $('#new-search').click(function () {
        var key = $("#newInput").val();
        var type = $("#sType").val();
        var msg = $('#newInput').attr('placeholder');
        if ($.trim(key) == "") {
            errmsg(msg);
            return false;
        } else if ($.trim(key).length < 2) {
            errmsg('至少2个关键字');
            return false;
        } else {
            if (type == 0) {
                window.location.href = encodeURI(INDEX_URL + "search?" + "key=" + key + "&index=name");
            } else if (type == 1) {
                window.location.href = encodeURI(INDEX_URL + "search?" + "key=" + key + "&index=opername");
            } else if (type == 2) {
                window.location.href = encodeURI(INDEX_URL + "search?" + "key=" + key + "&index=address");
            } else if (type == 3) {
                window.location.href = encodeURI(INDEX_URL + "search?" + "key=" + key + "&index=scope");
            } else if (type == 4) {
                window.location.href = encodeURI(INDEX_URL + "search?" + "key=" + key + "&index=featurelist");
            }
        }
    });

    $('#relation-nv a').click(function () {
        $(".newlist").hide();
        var key = $("#newInput").val();
        var type = $("#sType").val();
        //$(this).addClass("on");
        if (type == 1) {
            $('#newInput').attr('placeholder', '请输入准确的身份证号码')
        } else {
            $('#newInput').attr('placeholder', '请输入完整的企业名称')
        }
    });


    $('#relation-search').click(function () {
        var key = $("#newInput").val();
        var type = $("#sType").val();
        var msg = $('#newInput').attr('placeholder');
        if ($.trim(key) == "") {
            errmsg(msg);
            return false;
        } else if ($.trim(key).length < 2) {
            errmsg('至少2个关键字');
            return false;
        } else {
            if (type == 0) {
                window.location.href = encodeURI(INDEX_URL + "relation_search?" + "key=" + key);
            } else if (type == 1) {
                window.location.href = encodeURI(INDEX_URL + "relation_buy?" + "key=" + key);
            }
        }
    });

    //快报资讯
    $('#panel-news').hover(
        function () {
            $(this).css("overflow", "auto");
        }, function () {
            $(this).css("overflow", "hidden");
        });

    $('.item-inner').click(function () {
        // alert(123);
        if ($(this).children(".item-info").is(':hidden')) {
            //alert(123);
            $(".item-info").hide();
            $(this).children(".item-info").show();
        } else {
            $(this).children(".item-info").hide();
        }
    });

})


function selectType(typeIndex) {
    var container = document.getElementById("search-nv");
    var links = container.getElementsByTagName("a");
    if (!links) {
        return
    }
    document.getElementById("sType").value = typeIndex;
    for (i = 0; i < links.length; i++) {
        if (i == typeIndex) {
            links[i].className = "search-type  on"
        } else {
            links[i].className = "search-type "
        }
    }
}

function realtionType(typeIndex) {
    var container = document.getElementById("relation-nv");
    var links = container.getElementsByTagName("a");
    if (!links) {
        return
    }
    document.getElementById("sType").value = typeIndex;
    for (i = 0; i < links.length; i++) {
        if (i == typeIndex) {
            links[i].className = "searchType on"
        } else {
            links[i].className = "searchType"
        }
    }
}


/*	搜索结果 */
$(function () {
    var btn_timer = null;
    $('.filter-bar .btn-group').hover(
        function (event) {
            clearTimeout(btn_timer);
            $(".btn-group .dropdown-menu").hide();
            $(this).children(".dropdown-menu").show();
        }, function () {
            btn_timer = setTimeout(function () {
                $(".btn-group .dropdown-menu").hide();
            }, 500);
        });
});


$(function () {
    var btn_timer = null;
    $('.dropdown-submenu').hover(
        function (event) {
            clearTimeout(btn_timer);
            $("#hangye .dropdown-menu").hide();
            $(this).children(".dropdown-menu").show();
        }, function () {
            btn_timer = setTimeout(function () {
                $(".btn-group .dropdown-menu").hide();
            }, 500);
        });
});


//关注
function follow(obj, companykey) {
    $.ajax({
        type: 'post',
        url: INDEX_URL + '/company_followadd?companykey=' + companykey,
        success: function (data) {
            sucdia({content: "你关注了一家公司~ 萌萌哒~~"});
            obj.className = "btn btn-icon btn-success  btn-rounded btn-inactive m-r-xs";
            $(obj).attr('onclick', 'unfollow(this,"' + companykey + '");stopPP(arguments[0]);');
            $(obj).attr('title', '取消关注公司');
        },
    });
}


//取消关注
function unfollow(obj, companykey) {
    $.ajax({
        type: 'post',
        url: INDEX_URL + '/company_followdel?companykey=' + companykey,
        success: function (data) {
            obj.className = "btn btn-icon btn-default  btn-rounded btn-inactive m-r-xs";
            $(obj).attr('onclick', 'follow(this,"' + companykey + '");stopPP(arguments[0]);');
            $(obj).attr('title', '关注公司');
        },
    });
}


//阻止冒泡的方法
function stopPP(e) {
    var evt = e || window.event;
    //IE用cancelBubble=true来阻止而FF下需要用stopPropagation方法
    evt.stopPropagation ? evt.stopPropagation() : (evt.cancelBubble = true);
}


//发表产品评论
function postRroductComment() {
    var companykey = $("#companykey").val();
    var content = $("#commentcontent").val();
    var contentid = $("#contentid").val();
    if (content == '') {
        faldia({
            content: "请输入评论内容"
        });
        return false;
    } else {
        $.ajax({
            type: 'POST',
            url: INDEX_URL + '/user_productcommentAdd',
            data: 'companykey=' + companykey + '&content=' + content + '&contentid=' + contentid,
            success: function (msg) {
                var obj = JSON.parse(msg);
                if (obj.success == true) {
                    sucdia({content: "你评论了一家产品~ +5 积分！"});
                    productcomment(1);
                    $("#commentcontent").val('');
                } else {
                    faldia({
                        content: '亲，好像出什么错了，请稍后重试'
                    });
                }
            }
        })
    }

}

//删除评论
function delRroductComment(id) {
    $.post(INDEX_URL + '/company_productcommentDel?id=' + id, function (rs) {
        if (rs.success)  sucdia({
            content: "删除成功",
            'fn': function () {
                productcomment(1);
            }
        });
        else {
            faldia({
                content: rs.msg,
                'fn': function () {
                    if (rs['code'] == 1) {
                        location.href = INDEX_URL + "/user_login";
                    }
                }
            });
        }
    }, 'json');

}

//评论分页
function productcomment(page) {
    var contentid = $("#contentid").val();
    var url = INDEX_URL + "user_productfeeds?" + "contentid=" + contentid + "&p=" + page;
    $.ajax({
        type: 'GET',
        dataType: "html",
        url: url,
        success: function (data) {
            //alert(data);
            if (data) {
                $("#comment").html(data);
            }
        }
    })
}


//关注产品
function productfollow(obj, contentid) {
    $.ajax({
        type: 'post',
        url: INDEX_URL + '/user_productfollowadd?contentid=' + contentid,
        success: function (data) {
            sucdia({content: "你关注了一个产品~ 萌萌哒~~"});
            //obj.className = "btn btn-icon btn-success  btn-rounded btn-inactive m-r-xs";
            $(obj).attr('onclick', 'productunfollow(this,"' + companykey + '");stopPP(arguments[0]);');
            $(obj).text('取消关注');
        },
    });
}


//取消关注产品
function productunfollow(obj, contentid) {
    $.ajax({
        type: 'post',
        url: INDEX_URL + '/user_productfollowdel?contentid=' + contentid,
        success: function (data) {
            //obj.className = "btn btn-icon btn-primary  btn-rounded btn-inactive m-r-xs";
            $(obj).attr('onclick', 'productfollow(this,"' + contentid + '");stopPP(arguments[0]);');
            $(obj).text('+ 加关注');
        },
    });
}

//广告内容
window.onload = function () {
    if (getCookie("footad") == 0) {
        $("#float_mask").hide();
        $(".guider").hide();
    } else {
        $(".guider").show();
        $("#float_mask").show();
    }
}
//关闭底部广告 
function closeFootAd() {
    $(".guider").hide();
    $("#float_mask").hide();
    setCookie("footad", "0");
}

//设置cookie  
function setCookie(name, value) {
    var exp = new Date();
    exp.setTime(exp.getTime() + 1 * 60 * 60 * 1000);//有效期1小时
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}
//取cookies函数  
function getCookie(name) {
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
    if (arr != null) return unescape(arr[2]);
    return null;
}


//找关系
function findRelation(name) {
    // alert(name);
    $("#findModal").show();
    if ($(".tag").length == 0) {
        // alert(123);
        $(".tagsinput").html("");
    }
    if ($("#tag" + name + "").length == 1) {
        errmsg('节点已添加');
        return false;
    }

    var id = $(".tag").length;
    // alert(id);
    if (id > 4) {
        errmsg('至多选择五个节点');
        return false;
    }
    $(".tagsinput").append('<span class="tag ' + id + '"" id="tag' + name + '" onclick="removeTag(' + id + ')"><span>' + name + ' </span><a class="tagsinput-remove-link fui-cross-16"></a></span>');
    $(".btn-remove").css("display", "inline-block");
}

function findModal() {
    $("#findModal").show();
}

function hidefindModal() {
    $("#findModal").hide();
}

function removeTag(obj) {
    $(".tag." + obj + "").remove();
    // alert(e);
    if ($(".tag").length == 0) {
        // alert(123);
        $(".tagsinput").html('请点击左边 <span class="find-btn"><i class="fa   fa-plus-circle"></i></span> 加入 人或者公司 来找关系');
    }
}

function removeAllTag() {
    $(".tag").remove();
    $(".btn-remove").hide();
    $(".tagsinput").html('请点击左边 <span class="find-btn"><i class="fa   fa-plus-circle"></i></span> 加入 人或者公司 来找关系');
}

function findTo() {
    if ($(".tag").length < 2) {
        errmsg('至少选择两个节点');
        return false;
    }
    var searchKey = $(".tag").text();
    var url = encodeURI(INDEX_URL + "more_findRelation?searchKey=" + searchKey);
    window.open(url, "_blank");
}

//公司列表ajax请求
function getAjaxList(page) {
    var key = $("input[name='key']").val();
    var index = $("input[name='index']").val();
    var statuscode = $("input[name='statuscode']").val();
    var registCapiBegin = $("input[name='registCapiBegin']").val();
    var registCapiEnd = $("input[name='registCapiEnd']").val();
    var sortField = $("input[name='sortField']").val();
    var isSortAsc = $("input[name='isSortAsc']").val();
    var province = $("input[name='province']").val();
    var startDateBegin = $("input[name='startDateBegin']").val();
    var startDateEnd = $("input[name='startDateEnd']").val();
    var city = $("input[name='city']").val();
    var industrycode = $("input[name='industrycode']").val();
    var subindustrycode = $("input[name='subindustrycode']").val();
    var tel = $("input[name='tel']").val();
    var email = $("input[name='email']").val();
    var ajaxflag = $("input[name='ajaxflag']").val();
    if (registCapiBegin == 0)registCapiBegin = '';
    if (registCapiEnd == 0)registCapiEnd = '';
    $("input[name='page']").val(page);
    $('#load_data').show();
    $('#ajaxlist').hide();
    $.ajax({
        url: INDEX_URL + '/search_index',
        type: 'get',
        data: {
            key: key,
            index: index,
            statusCode: statuscode,
            registCapiBegin: registCapiBegin,
            registCapiEnd: registCapiEnd,
            sortField: sortField,
            isSortAsc: isSortAsc,
            province: province,
            startDateBegin: startDateBegin,
            startDateEnd: startDateEnd,
            cityCode: city,
            industryCode: industrycode,
            subIndustryCode: subindustrycode,
            tel: tel,
            email: email,
            ajaxflag: ajaxflag,
            p: page
        },
        dataType: 'html',
        success: function (result) {
            $('#ajaxlist').html(result);
            var sortDesc = $("input[name='hiddenSort']").val();
            if (sortDesc != '')$('.sortDesc').text(sortDesc);
            var hiddenArr = ['Statuscode', 'RegistCapi', 'Startdate', 'Province', 'City', 'Industrycode', 'Subindustrycode', 'Tel', 'Email'];
            var appendHide = true;
            appendSearchWord(hiddenArr);
            //如果没有搜索条件，隐藏公司列表上方的筛选条件DIV
            $('#appendBox .appendSpan').each(function () {
                if ($(this).css('display') != 'none') {
                    appendHide = false;
                    return false;
                }
            });
            if (appendHide) {
                $('#appendBox').prev().css('margin-bottom', '20px');
                $('#appendBox').hide();
            } else {
                $('#appendBox').prev().css('margin-bottom', '0px');
                $('#appendBox').show();
            }
            $('#load_data').hide();
            $('html, body').animate({scrollTop: 0}, 'normal');
            $('#ajaxlist').show();
        },
        error: function (result) {
            console.log(result);
        }
    });
}
//公司列表ajax请求
function getAjaxList2(page) {
    var key = $("input[name='key']").val();
    var index = $("input[name='index']").val();
    var statuscode = $("input[name='statuscode']").val();
    var sortField = $("input[name='sortField']").val();
    var isSortAsc = $("input[name='isSortAsc']").val();
    var cat = $("input[name='cat']").val();
    var startDateBegin = $("input[name='startDateBegin']").val();
    var startDateEnd = $("input[name='startDateEnd']").val();
    var flowno = $("input[name='flowno']").val();
    var ajaxflag = $("input[name='ajaxflag']").val();
    $("input[name='page']").val(page);
    $('#load_data').show();
    $('#ajaxlist').hide();
    $.ajax({
        url: INDEX_URL + '/more_brand',
        type: 'get',
        data: {
            key: key,
            index: index,
            status: statuscode,
            sortField: sortField,
            isSortAsc: isSortAsc,
            flowno: flowno,
            startDateBegin: startDateBegin,
            startDateEnd: startDateEnd,
            cat: cat,
            ajaxflag: ajaxflag,
            p: page
        },
        dataType: 'html',
        success: function (result) {
            $('#ajaxlist').html(result);
            var sortDesc = $("input[name='hiddenSort']").val();
            if (sortDesc != '')$('.sortDesc').text(sortDesc);
            var hiddenArr = ['Statuscode', 'Startdate', 'Flowno', 'Cat'];
            var appendHide = true;
            appendSearchWord(hiddenArr);
            //如果没有搜索条件，隐藏公司列表上方的筛选条件DIV
            $('#appendBox .appendSpan').each(function () {
                if ($(this).css('display') != 'none') {
                    appendHide = false;
                    return false;
                }
            });
            if (appendHide) {
                $('#appendBox').prev().css('margin-bottom', '20px');
                $('#appendBox').hide();
            } else {
                $('#appendBox').prev().css('margin-bottom', '0px');
                $('#appendBox').show();
            }
            $('#load_data').hide();
            $('html, body').animate({scrollTop: 0}, 'normal');
            $('#ajaxlist').show();
        },
        error: function (result) {
            console.log(result);
        }
    });

}
//把筛选条件单独显示出来
function appendSearchWord(hiddenArr) {
    var sname = '';
    var sclass = '';
    var svalue = '';

    for (var i = 0; i < hiddenArr.length; i++) {
        sname = "input[name='hidden" + hiddenArr[i] + "']";
        svalue = $(sname).val();
        sclass = '.append' + hiddenArr[i];
        if (svalue != '') {
            svalue = svalue + '<span class="glyphicon glyphicon-remove" style="padding-left: 3px"></span>';
            $(sclass).html(svalue);
            $(sclass).show();
        } else {
            $(sclass).hide();
        }
    }
}

//企业服务评论分页
function getServiceComment(page, id) {
    $.ajax({
        data: {p: page, id: parseInt(id), ajax: true},
        url: INDEX_URL + 'store_view',
        type: 'get',
        dataType: 'html',
        success: function (result) {
            if (result) {
                $('#commentlist').html(result);
            }
        }
    });
}

//添加企业服务评论
function addServiceComment() {
    var serviceid = $("#serviceid").val();
    var content = $('#commentcontent').val();
    if (content == '') {
        faldia({
            content: "请输入评论内容"
        });
        return false;
    } else {
        $.ajax({
            type: 'POST',
            url: INDEX_URL + '/store_addComment',
            data: {id: serviceid, content: content},
            success: function (msg) {
                if (msg.success == true) {
                    sucdia({content: "你评论了一家公司~ 获得 5 积分！"});
                    getServiceComment(1, serviceid);
                    $("#commentcontent").val('');
                } else {
                    faldia({
                        content: '亲，好像出什么错了，请稍后重试'
                    });
                }
            }
        })
    }
};

function deleteServiceComment(commentid, serviceid) {
    $.ajax({
        data: {commentid: commentid, serviceid: serviceid},
        url: INDEX_URL + '/store_deleteComment',
        type: 'post',
        success: function (result) {
            if (result.success) {
                sucdia({
                    content: "删除成功",
                    'fn': function () {
                        getServiceComment(1, serviceid);
                    }
                });
            } else {
                faldia({
                    content: result.msg,
                    'fn': function () {

                    }
                });
            }
        }
    });
};

//公司产品发表评论
function addProductComment() {
    var content = $("#commentcontent").val();
    if (content == '') {
        faldia({content: "请输入评论内容"});
        return false;
    } else {
        $.ajax({
            type: 'POST',
            url: INDEX_URL + '/company_commentAdd',
            data: $("#addProductComment").serialize(),
            success: function (msg) {
                if (msg.success == true) {
                    sucdia({content: "你评论了一家公司~ 获得 5 积分！"});
                    getProductComment(1, $("input[name='commentcode']").val());
                    $("#commentcontent").val('');
                } else {
                    faldia({
                        content: '亲，好像出什么错了，请稍后重试'
                    });
                }
            }
        })
    }
}

//删除公司产品评论
function deleteProductComment(commentcode, companykey, commentid) {
    $.post(INDEX_URL + '/company_commentDel?id=' + commentcode + '&companykey=' + companykey + '&commentid=' + commentid, function (rs) {
        if (rs.success)  sucdia({
            content: "删除成功",
            'fn': function () {
                getProductComment(1, commentcode);
            }
        });
        else {
            faldia({
                content: rs.msg,
                'fn': function () {
                    if (rs['code'] == 1) {
                        location.href = INDEX_URL + "/user_login";
                    }
                }
            });
        }
    }, 'json');
}

//公司产品评论分页
function getProductComment(page, id) {
    $.ajax({
        data: {p: page, ajax: true, id: id},
        url: INDEX_URL + 'product_index',
        type: 'get',
        dataType: 'html',
        success: function (result) {
            if (result) {
                $('#commentlist').html(result);
            }
        }
    });
}

function searchKeydown(event, obj) {
    var event = event || window.event;
    var keyCode = event.keyCode;//40:下移，38：上移
    var flag = false;
    //var list = obj == 1 ? $('#search-list') : $('#header-search-list');
    var list = obj == 3 ? $('#radar-search-list') : (obj == 1 ? $('#search-list') : $('#header-search-list'));
    //var key = obj == 1 ? $('#searchkey') : $('#headerKey');
    var key = obj == 3 ? $('#radarkey') : (obj == 1 ? $('#searchkey') : $('#headerKey'));
    var radarFlag = obj == 3 ? true : false;
    //搜索列表是否显示
    var isShow = list.css('display');
    if (isShow == 'block' && (keyCode == 40 || keyCode == 38)) {
        //判断是否有选中公司
        list.find('a').each(function (i) {
            if ($(this).hasClass('keyMove')) {
                $(this).removeClass('keyMove');
                if (i != 4 && keyCode == 40) {
                    var nextObj = list.find('a').eq(i + 1);
                    var nextObjSpanText = list.find('a').eq(i + 1).find('span').text();
                    assignSearchkey(key, nextObj, nextObjSpanText, radarFlag);
                    flag = true;
                }
                if (i != 0 && keyCode == 38) {
                    var nextObj = list.find('a').eq(i - 1);
                    var nextObjSpanText = list.find('a').eq(i - 1).find('span').text();
                    assignSearchkey(key, nextObj, nextObjSpanText, radarFlag);
                    flag = true;
                }
                return false;//跳出each循环
            }
        });
        if (!flag) {
            var j = keyCode == 40 ? 0 : 4;
            var nextObj = list.find('a').eq(j);
            var nextObjSpanText = list.find('a').eq(j).find('span').text();
            assignSearchkey(key, nextObj, nextObjSpanText, radarFlag);
        }
    }
}

function assignSearchkey(key, nextObj, nextObjSpanText, radarFlag) {
    //样式变化
    nextObj.addClass('keyMove');
    //值处理
    var text = nextObj.text();
    text = text.replace(nextObjSpanText, '');
    //修改值
    key.val(text);
    //修改公司ID
    if (radarFlag) {
        var companykey = nextObj.attr('data-key');
        $("input[name='radarCompanykey']").val(companykey);
    }
}



