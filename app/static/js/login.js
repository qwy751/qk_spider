/**
 * Created by fruit on 2016/11/21.
 */
$(function () {
    $(".image-block").backstretch(
        [
            "../static/img/login/slider1.jpg",
            "../static/img/login/slider2.jpg",
            "../static/img/login/slider3.jpg",
            "../static/img/login/slider4.jpg",
            "../static/img/login/slider5.jpg",
        ],
        {
            fade: 1000,
            duration: 7000
        }
    );

    function changeStyle(elem) {
        if (elem.html() == "进入&gt;&gt;") {
            elem.html("登录中...").attr("disabled", "disabled");
        } else {
            elem.html("进入&gt;&gt;").removeAttr("disabled");
        }
    }

    function message(elem, msg) {
        elem.removeAttr("style").html("<i class='glyphicon glyphicon-exclamation-sign'></i>" + msg);
        $('#sub_btn').html("进入&gt;&gt;").removeAttr("disabled");
    }
    function message1(elem, msg) {
        elem.removeAttr("style").html("<i class='glyphicon glyphicon-exclamation-sign'></i>" + msg).fadeOut(3000);
    }

    // 使用 jQuery 异步提交表单

    $('#sub_btn').click(function () {
        var value = $("#username").val();
        var password = $("#password").val();
        var elem = $("#msg-error");
        var msg1 = "请输入有效的登录名";
        var msg2 = "请输入登录名";
        var msg3 = "密码长度不够";
        var msg4 = "请输入密码";

        console.log(value.length);
        console.log(password.length);
        if(value.length > 2 && password.length > 2){
            changeStyle($(this));
            jQuery.ajax({
                url: '/login/user',
                data: $('#logInForm').serializeArray(),
                type: "POST",
                error: function () {
                    $(".cover").hide();
                },
                success: function (data) {
                    $(".cover").hide();
                    //code服务端返回的状态码
                    var code = data.code;
                    var elem = $("#msg-error");
                    var msg00 = "账号不存在，请重新输入";
                    var msg01 = "密码错误，请重新输入";
                    var msg20 = "请输入验证码";
                    var msg21 = "验证码为空，请重新输入";
                    var msg22 = "验证码错误，请重新输入";
                    var msg05 = "账号未激活！";
                    var msg06 = "系统错误";
                    switch (code) {
                        // 200 登录成功
                        case 200 :
                            window.location.href = '/index';
                            break;
                        // 0 账号不存在
                        case 0 :
                            message(elem, msg00);
                            break;
                        // 1 密码错误
                        case 1 :
                            message(elem, msg01);
                            break;
                        // 2 验证码为空或错误
                        case 2 :
                            if (data.message == "null") {
                                if ($("#checkCodeDiv").css("display") == "none") {
                                    $("#checkCodeDiv").removeClass("display");
                                    $("#checkCode").html("<img style='width:150px;height:60px' class='imgClick' src='/kaptcha' alt='看不清楚,点击更换'>");
                                    message(elem, msg20);
                                } else {
                                    message(elem, msg21);
                                }
                            } else {
                                message(elem, msg22);
                            }
                            ;
                            break;
                        // 3 剩余登录次数
                        case 3 :
                            var msg03 = "密码错误，您今天还剩余" + data.message + "次登录次数";
                            message(elem, msg03);
                            $("#checkCodeDiv").removeClass("display");
                            $("#checkCode").html("<img style='width:150px;height:60px' class='imgClick' src='/kaptcha' alt='看不清楚,点击更换'>");
                            break;
                        // 4 距离下次登录剩余时间
                        case 4 :
                            var msg04 = "距离下次登录还剩余" + data.message;
                            message(elem, msg04);
                            break;
                        // 5 账号未激活
                        case 5 :
                            message(elem, msg05);
                            break;
                        // 6 系统端错误
                        case 6 :
                            message(elem, msg06);
                            break;
                    }
                }
            });
        }else if(value.length < 4 && value.length > 0){
            message1(elem, msg1);
        }else if(value.length == 0){
            message1(elem, msg2);
        }else if(password.length < 3 && password.length > 0){
            message1(elem, msg3);
        }else if(password.length == 0){
            message1(elem, msg4);
        }
    });

    $(".fa-wechat").hover(function () {
            var pos = $(this).position();
            var pos_x = pos.left-50;
            var pos_y = pos.top-180;
            $("#chat").css({ "display": "block",'left' : pos_x, 'top' : pos_y})
        },
        function () {
            $("#chat").css({ "display": "none" });
        });



})
