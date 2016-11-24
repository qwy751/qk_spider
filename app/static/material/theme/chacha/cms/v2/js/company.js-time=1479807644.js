/*搜索结果页面*/
$(function(){

    changetab();

    var key         = $("#companyname").val();
    var companykey  = $("#unique").val();
    var companylogo = $("#companylogo").val();
    var isrecompany  = $("#isrecompany").val();

    if(companylogo!=""){
        // alert(123);
        getLogo(companykey,companylogo);
    }

    /*导航栏悬浮*/
    $(window).scroll(function() {
  /*      if($(window).scrollTop() >= 200){
            $("#company-nav").addClass("fixed_nav");
        }else{
            $("#company-nav").removeClass("fixed_nav");
        }*/
    });

})

/*公司导航栏切换标签*/

function changetab(){
    var hash = location.hash;
    //alert(hash);
    if(hash!=""){
        $(hash+"_title").click();
        //  alert(hash);
        //alert(hash);
    }else{
        $("#base_title").click();
        //alert(hash);
    }
}


$("a[tabid]").click(function() {
    var unique       = $("#unique").val();
    var companyname  = $("#companyname").val();
    //alert(companyname);
    var tabid = $(this).attr("tabid");
    // alert(tabid);
    var data_info=$("."+tabid+"_info");
    var hash = location.hash;
    if(hash!=""||tabid!="base"){
        window.location.hash = "#" + tabid;
        $("#ziben-list").hide();
        $("#news-list").hide();
    }
    if(hash==""||tabid=="base"){
        $("#ziben-list").show();
        $("#news-list").show();
    }

    $("a[tabid]").removeClass("current");
    $("a[tabid="+tabid+"]").addClass("current");
    // alert(data_info.size());
    if(data_info.size()==0){
	    $("#load_data").show(); 		
        getDetail(tabid,unique,companyname);
        showdata(tabid);
    }else{
        showdata(tabid);
    }
});

function getDetail(tabid,unique,companyname){
    unique      = encodeURIComponent(unique);
    companyname = encodeURIComponent(companyname);
    var path = INDEX_URL+"company_getinfos?";
    //alert(tabid);
    var url = path+"unique="+unique+'&companyname='+companyname+'&tab='+tabid;
    $.ajax({
        type:'GET',
        dataType:"html",
        url:url,
        success:function(data){
            if(data){
                showdata(tabid);
                $("#load_data").hide();
                $("#"+tabid+"_div").html(data);
            }
        }
    })

}


function showdata(tabid){
    $(".data_div").css("display", "none");
    $("#"+tabid+"_div").css("display", "block");
    window.scrollTo(0,0);
}



/*获取公司LOGO*/
function getLogo(companykey,companylogo){
    // alert(companykey);
    $.ajax({
        type:'GET',
        url:INDEX_URL+'/company_logo',
        data:'unique='+companykey+'&companylogo='+companylogo,
        success:function(msg){
            //alert("11"+msg);
            var obj = JSON.parse(msg);
            if(obj.status==0){
                return false;
            }else{
                $("#companybiglogo").attr("src","http://co-image.qichacha.com/CompanyImage/"+companykey+".jpg");
            }
        }
    })
}

//切换到添加新分组
$('#newGroup').on('click',function(){
   $(this).parent().parent().hide();
   $(this).parent().parent().next().show();
});

//切换到添加老分组
$('#oldGroup').on('click',function(){
    $(this).parent().parent().hide();
    $(this).parent().parent().prev().show();
});

//关注公司
$('#chooseGroup').on('click', function () {
    var companykey = $('#groupCompanykey').val();
    var obj = '#follow';
    var group = $('#groupId').val();
    if($(obj).attr('data-flag') == 0 && group != ''){
        follow($(obj),companykey,group);
    }else{
        faldia({content:'请选择分组'});
        return false;
    }
});

//添加新分组并关注公司
$('#addGroup').on('click',function(){
    var groupname = $('#addGroupName').val();
    var companykey = $('#groupCompanykey').val();
    var url = INDEX_URL+'company_addgroup';
    if(groupname == '')return false;
    $.ajax({
        data:{groupname:groupname},
        type:'post',
        url:url,
        success:function(result){
            console.log(result);
            if(result.success){
                follow($('#follow'),companykey,result.list.follow_group_id);
            }else{
                faldia({content:result.msg});
            }
        }
    });
});

function getGrouplist(){
    var groupArr = [];
    var groupCount = 0;
    $.ajax({
        data:{},
        url:'/company_getgrouplist',
        type:'get',
        success:function(result){
            $.map(result.list,function(item,i){
                if(i == 0) {
                    groupArr[i] =
                        '<li data-value="' + item.follow_group_id + '">' +
                        item.group_name +
                        '<span class="glyphicon glyphicon-ok"></span></li>';
                    $('#groupId').val(item.follow_group_id);
                }else{
                    groupArr[i] =
                        '<li data-value="' + item.follow_group_id + '">' +
                        item.group_name +
                        '<span class="glyphicon"></span></li>';
                }
                groupCount += 1;
            });
            $('.groupBox').html(groupArr);
            $('.groupCount').html(groupCount);
            $('.groupBox li').on('click',function(){
                $('.groupBox').find('span').removeClass('glyphicon-ok');
                $(this).find('span').addClass('glyphicon-ok');
                var groupid = $(this).attr('data-value');
                $('#groupId').val(groupid);
            });
        }
    });
}

//关注
function  follow(obj,companykey,group){
    $.ajax({
        type: 'post',
        data:{companykey:companykey,group:group},
        url: INDEX_URL+'/company_followadd',
        success: function(data){
            if(!data.success){
                faldia({content:data.msg});
                return false;
            }
            $('#closeGroupBox').click();
            sucdia({content:"你关注了一家公司~ 萌萌哒~~"});
            //obj.className = "btn btn-icon btn-primary  btn-rounded btn-inactive m-r-xs";
            $(obj).removeClass('btn-default');
            $(obj).addClass('btn-primary');
            $(obj).attr('onclick','unfollow(this,"'+companykey+'");');
            $(obj).attr('title','取消关注');
            $('.follow-text').text('已关注');
            $(obj).addClass('btn-primary');
            $(obj).find('.fa').removeClass('fa-plus');
            $(obj).find('.fa').addClass('fa-check');
            $(obj).attr('data-toggle','');
            $(obj).attr('data-target',''); 
            $(obj).attr('data-flag',1);
        }
    });
}



//取消关注
function  unfollow(obj,companykey){
    $.ajax({
        type: 'post',
        url: INDEX_URL+'/company_followdel?companykey='+companykey,
        success: function(data){
            //obj.className = "btn btn-icon btn-default  btn-rounded btn-inactive m-r-xs";
            $(obj).removeClass('btn-primary');
            $(obj).addClass('btn-default');
            $(obj).attr('onclick','getGrouplist()');
            $(obj).attr('title','关注公司');
            $('.follow-text').text('关注');
            $(obj).attr('data-toggle','modal');
            $(obj).find('.fa').addClass('fa-plus');
            $(obj).find('.fa').removeClass('fa-check');            
            $(obj).attr('data-target','#groupModal');
            $(obj).attr('data-flag',0);
        }
    });
}




//取消点赞
function unfav(obj,e,posturl){
    $.ajax({
        type: 'post',
        url: posturl+'/course_zandel?cid='+e,
        data: {unfav:'true'},
        success: function(data){
            obj.className = "upvote";
            oldnum = $(obj).find('.votenum').html();
            $(obj).find('.votenum').html(parseInt(oldnum)-1);
            $(obj).attr('onclick','fav(this,"'+e+'","'+posturl+'");stopPP(arguments[0]);');
        },
    });
}



//赞
$("#zanadd").click(function(){
    //alert($(this).attr('companykey'));
    $.post(INDEX_URL+'/company_zanadd?companykey='+ $(this).attr('companykey'),function(rs){
        if(rs.success){
            $("#like_count").html(parseInt($("#like_count").html()) + 1);
            sucdia({content:"你点了赞~ 萌萌哒~~"});
        }else{
            faldia({
                content: rs.msg,
                'fn': function() {
                    if (rs['code'] == 1){
                        location.href = INDEX_URL+"/user_login";
                    }
                }
            });
        }
    },'json');
});
//取消赞
$("#zandel").click(function(){
    $.post(INDEX_URL+'/company_zandel?companykey='+ $(this).attr('companykey'),function(rs){
        if(rs.success)  sucdia({content:"取消成功",'fn':function(){
            location .reload();
        }});
        else faldia({content:rs.msg});
    },'json');
});







//阻止冒泡的方法
function stopPP(e){
    var evt = e || window.event;
    //IE用cancelBubble=true来阻止而FF下需要用stopPropagation方法
    evt.stopPropagation ? evt.stopPropagation() : (evt.cancelBubble=true);
}









/*委托更新*/
function update(){
    var unique     =  $("#unique").val();
    // alert(unique);
    $(".change a").text('正在更新');
    $(".updatetext").text('正在更新');
    $.post(INDEX_URL+'/company_update?keyNo='+unique,function(rs){
        if(rs.Status==200){
            sucdia({
                content:"委托更新成功",
                'fn':function(){
                    location.reload()
                }
            });
        }else if(rs.Status==205){
            var jobid = rs.JobId;
            getJob(jobid,1);
        }else{
            faldia({
                content: rs.msg,
                'fn': function() {
                    location.reload();
                }
            });
        }
    },'json');
}


function getJob(JobId,count){
    //alert(JobId);
    $("#djs").show();
    $("#djs").text(count);
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_getByJob',
        data:'jobid='+JobId,
        success:function(jobmsg){
            //alert("2211"+jobmsg);
            var obj2 = JSON.parse(jobmsg);
            if(obj2.Status==200){
                sucText()
            }else if(obj2.Status==205){
                count++;
                if(count>60){
                    falText()
                }else{
                    time = setTimeout("getJob('"+obj2.JobId+"','"+count+"')",2000);
                    if(count>60){
                        clearTimeout(time);
                    }
                }
            }else{
                faldia({
                    content: '更新失败',
                    'fn': function() {
                        location.reload();
                    }
                });
            }
        }
    })
}


//请求年报
function askReport(){
    var unique     =  $("#unique").val();
    $("#noReport").hide();
    $("#loadReport").show();
    //alert($(this).attr('companykey'));
    $.get(INDEX_URL+'/company_askReport?keyNo='+ unique,function(rs){
        //alert(rs);
        if(rs.Status==200){
            sucdia({
                content:"请求成功",
                'fn':function(){
                    location.reload()
                }
            });
        }else if(rs.Status==205){
            var jobid = rs.JobId;
            getJobReport(jobid,1);
        }else{
            faldia({
                content: rs.msg,
                'fn': function() {
                    location.reload();
                }
            });
        }
    },'json');
}





/*轮回获取数据*/
function getJobReport(JobId,count){
    //alert(JobId);
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_getByJob',
        data:'jobid='+JobId,
        success:function(jobmsg){
            //alert("2211"+jobmsg);
            var obj2 = JSON.parse(jobmsg);
            if(obj2.Status==200){
                if(obj2.Result.AnnualReports.length>0){
                    sucdia({
                        content:"委托更新成功",
                        'fn':function(){
                            location.reload()
                        }
                    });
                }else{
                    faldia({
                        content: '目前还没有年报，请稍后重试',
                        'fn': function() {
                            location.reload();
                            $("#askReport").hide();
                        }
                    });
                }
                //sucText()
            }else if(obj2.Status==205){
                count++;
                if(count>60){
                    faldia({
                        content: '请稍后重试',
                        'fn': function() {
                            location.reload();
                        }
                    });
                }else{
                    time = setTimeout("getJobReport('"+obj2.JobId+"','"+count+"')",2000);
                    if(count>60){
                        clearTimeout(time);
                    }
                }
            }else{
                faldia({
                    content: '请求失败',
                    'fn': function() {
                        location.reload();
                    }
                });
            }
        }
    })
}



function sucText(){
    $(".change a").text('委托更新');
    $(".change").attr("disabled",true);
    sucdia({
        content:"委托更新成功",
        'fn':function(){
            location.reload()
        }
    });
}

function falText(){
    $(".change a").text('委托更新');
    $(".change").attr("disabled",true);
    faldia({
        content:"亲，不要着急，慢慢来哦！！！",
        'fn':function(){
            location.reload()
        }
    });
}



//发表评论
function postComment(tab){
    var tab = arguments[0] ? 'job' : 'base';
    var companykey     =  $("#unique").val();
    var content        =  $("#commentcontent").val();
    var email          =  $("#companyemail").val();
    if(content==''){
        faldia({
            content:"请输入评论内容"
        });
        return false;
    }else{
        $.ajax({
            type:'POST',
            url:INDEX_URL+'/company_commentAdd',
            data:'companykey='+companykey+'&content='+content+'&email='+email,
            success:function(msg){
                //console.log(msg.success);
                //var obj = JSON.parse(msg);
                if(msg.success==true){
                    sucdia({content:"你评论了一家公司~ 获得 5 积分！"});
                    if(tab == 'base'){
                        getTabList(1,'base','comment');
                    }else{
                        getTabList(1,'job','comment2');
                    }
                    $("#commentcontent").val('');
                }else{
                    faldia({
                        content: '亲，好像出什么错了，请稍后重试'
                    });
                }
            }
        })
    }

}





//删除评论
function delComment(id,companykey){
    $.post(INDEX_URL+'/company_commentDel?id='+id+'&companykey='+companykey,function(rs){
        if(rs.success)  sucdia({
            content:"删除成功",
            'fn':function(){
                getTabList(1,'base','comment');
            }
        });
        else{
            faldia({
                content: rs.msg,
                'fn': function() {
                    if (rs['code'] == 1){
                        location.href = INDEX_URL+"/user_login";
                    }
                }
            });
        }
    },'json');

}

//分享地址
var timestamp;var nonceStr;var signature;
function startRequest()
{
    var unique       = $("#unique").val();
    var companyname  = $("#companyname").val();

    var share = $('#qrcode').attr('data');
    if(share==1) return false;
    xmlHttp = new XMLHttpRequest();
    try
    {
        xmlHttp.onreadystatechange = handleStateChange;
        xmlHttp.open("GET", "http://wechat.qichacha.com/enterprises/w1/getShareURLForDetail?category=4&province=&companyName="+companyname+"&key="+unique, true);
        xmlHttp.send();
    }
    catch(exception)
    {
        alert("xmlHttp Fail");
    }
}
function handleStateChange()
{
    if(xmlHttp.readyState == 4)
    {
        if (xmlHttp.status == 200 || xmlHttp.status == 0)
        {
            var result = xmlHttp.responseText;

            var data = eval("(" + result + ")");
            // var shareUrl =  data.data;
            var str = data.data;
            $('#qrcode').qrcode(str);
            $('#qrcode').attr('data',1);
        }
    }
}


/*商标详情*/
function sbview(sbid){
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_shangbiaoView',
        data:'id='+sbid,
        success:function(msg){
            var html="";
            var obj = JSON.parse(msg);
            //alert("11"+msg);
            if(obj.Status=="200"){
                var html = shangbiaoHTML(obj.Result);
                $(".sbview").html(html);
            }else{
                $(".sbview").html("未找到相关商标信息");
            }
        }
    })
}

/**商标html**/
function shangbiaoHTML(data){
    var html='';
    html = html+"<table class='table table-bordered'>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>商标名称：</td><td colspan='5'>"+data.Name+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>注册号：</td><td>"+data.RegNo+"</td>";
    html = html+"<td  colspan='2'>"+data.CategoryId+" - "+data.Category+"</td>";
    html=html+"<td class='slabel'>商标状态：</td><td> "+data.FlowStatus+"</td>";
    html = html+"</tr>";
    html = html+"<tr  class='white'>";
    html = html+"<td class='slabel'>申请人：</td> <td  colspan='2'>"+data.Person+"</td>";
    html = html+"<td class='slabel'>申请日期：</td><td colspan='2'>"+data.ApplyDate+"</td>";
    html = html+"</tr>";
    html = html+"<tr  class='white'>";

    if(data.HasImage==true){
        html = html+"<td colspan='2'><img src='"+data.ImageUrl+"' style='max-width:200px;'/></td>";
    }else{
        if(data.Name){
            html=html+"<td colspan='2'><p class='no-img'>"+data.Name+" </p></td>";
        }else{
            html=html+"<td colspan='2'><p class='no-img'>暂无 </p></td>";
        }
    }
    html = html+"<td class='slabel text-center'>商<br>品<br>/<br>服<br>务<br>列<br>表</td>";
    html = html+"<td>";
    for(var i=0;i<data.ListGroupItems.length;i++){
        //alert(data.FlowItems.FlowItem);
        //alert(123);
        html=html+"<p>"+data.ListGroupItems[i]+"</p>";
    }
    html = html+"</td>";
    html = html+"<td class='slabel text-center'>商<br>标<br>流<br>程</td>";
    html = html+" <td>";
    for(var i=0;i<data.FlowItems.length;i++){
        //alert(data.FlowItems.FlowItem);
        //alert(123);
        html=html+"<p>";
        if(data.FlowItems[i].FlowDate){
            html = html+""+data.FlowItems[i].FlowDate+"";
        }
        html  = html+"&nbsp;&nbsp;"+data.FlowItems[i].FlowItem+"";
        html  = html+"</p>";
    }
    html = html+"</td>";

    html = html+"</tr>";

    html = html+"<tr  class='white'>";
    html = html+"<td  colspan='1' class='slabel'>使用期限：</td>";
    html = html+"<td colspan='2'>"+data.ValidPeriod+" </td>";
    html = html+"<td colspan='1' class='slabel'>代理机构：</td>";
    if(data.Agent){
        html = html+"<td colspan='2'>"+data.Agent+"</td>";
    }else{
        html = html+"<td colspan='2'></td>";
    }
    html = html+"</tr>";
    html  = html+"</table>";
    return html;
}

/*专利详情*/
function zlView(zlid){
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_zhuanliView',
        data:'id='+zlid,
        success:function(msg){
            var html="";
            var obj = JSON.parse(msg);
            // alert("11"+msg);
            if(obj.Result){
                var html = zhuanliHTML(obj.Result);
                $(".zlview").html(html);
            }else{
                $(".zlview").html("未找到相关信息");
            }
        }
    })
}




function zhuanliHTML(data){
    var html='';
    html = html+"<table class='table table-bordered'>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel' style='width:15%;'>名称：</td><td colspan='3'>"+data.Title+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>申请号：</td> <td>"+data.ApplicationNumber+"</td>";
    html = html+"<td class='slabel'>申请日：</td><td>"+data.ApplicationDate+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>申请公布号：</td> <td>"+data.PublicationNumber+"</td>";
    html = html+"<td class='slabel'>申请公布日：</td><td>"+data.PublicationDate+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>发明人：</td>";
    html = html+"<td>"
    $.each(data.InventorStringList,function(i,value){
        html = html+""+value+"&nbsp;&nbsp;";
    });
    html = html+"</td>";
    html = html+"<td class='slabel'>类型：</td><td>"+data.KindCodeDesc+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>专利代理机构：</td> <td>"+data.Agency+"</td>";
    html = html+"<td class='slabel'>法律状态：</td><td>"+data.LegalStatusDesc+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel' style='width:15%;'>法律历史状态：</td><td colspan='3'>";
    $.each(data.PatentLegalHistory,function(i,item){
        html = html+""+item.Desc+"&nbsp;&nbsp;"+item.LegalStatusDate+"&nbsp;&nbsp;";
    });
    html = html+"</td>";
    html = html+"</tr>";
    html = html+"<tr class='white'>";
    html = html+"<td class='slabel'>摘要：</td><td colspan='3'>"+data.Abstract+"</td>";
    html = html+"</tr>";
    html  = html+"</table>";
    return html;
}

/*证书详情*/

function zsView(zsid){
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_zhengshuView',
        data:'id='+zsid,
        success:function(msg){
            var html="";
            var obj = JSON.parse(msg);
            // alert("11"+msg);
            if(obj.status=="200"){
                var html = zhengshuHTML(obj.data);
                $(".zsview").html(html);
            }else{
                $(".zsview").html("未找到相关信息");
            }
        }
    })
}



function zhengshuHTML(data){
    var html='';
    html = html+"<table class='table table-bordered'>";
    $.each(data.Data,function(i,value){
        if(i!='_id'&&i!='_status'&&i!='_title'&&i!='_type'){
            html = html+"<tr class='white'>";
            html = html+"<td class='slabel' style='width:18%;'>"+i+"</td><td colspan='3'><div style='word-wrap: break-word; word-break: break-all; '>"+value+"</div></td>";
            html = html+"</tr>";
        }
    });

    html  = html+"</table>";
    return html;
}




/*著作权详情*/
function zzqView(zsid){
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_zhuanliView',
        data:'id='+zsid,
        success:function(msg){
            var html="";
            var obj = JSON.parse(msg);
            // alert("11"+msg);
            if(obj.status=="200"){
                var html = zzqHTML(obj.data);
                $(".zzqview").html(html);
            }else{
                $(".zzqview").html("未找到相关信息");
            }
        }
    })
}



function zzqHTML(data){
    var html='';
    html = html+"<table class='table table-bordered'>";
    $.each(data,function(i,value){
        if(i!='_id'&&i!='_status'&&i!='_title'&&i!='_type'){
            html = html+"<tr class='white'>";
            html = html+"<td class='slabel' style='width:18%;'>"+i+"</td><td colspan='3'><div style='word-wrap: break-word; word-break: break-all; '>"+value+"</div></td>";
            html = html+"</tr>";
        }
    });

    html  = html+"</table>";
    return html;
}


/*裁判文书详情*/
function wsView(wsid){
    $.ajax({
        type:'POST',
        url:INDEX_URL+'/company_wenshuView',
        data:'id='+wsid,
        success:function(msg){
            var html="";
            var obj = JSON.parse(msg);
            // alert("11"+msg);
            if(obj.status=="200"){
                var html = obj.data;
                //alert(html);
                $("#wsview").html(html);
            }else{
                $("#wsview").html("未找到相关信息");
            }
        }
    })
}

function showmap(){

    /*弹窗大地图*/
    var map = new BMap.Map("allmap");
    map.addControl(new BMap.NavigationControl());
    map.addControl(new BMap.MapTypeControl());
    map.addControl(new BMap.OverviewMapControl());
    map.enableScrollWheelZoom(true);
    // 创建地址解析器实例
    var gc = new BMap.Geocoder();
    $(function(){
        $('#mapPreview').bind('click',function(){
            //$.colorbox({inline:true, href:"#baiduMap",title:"公司地址"});
            var address = "{{$company.Address}}";
            var city = "{{$shen}}";
            var lat = $('#positionLat').val();
            var lng = $('#positionLng').val();
            map.setCurrentCity(city);
            map.setZoom(12);
            gc.getPoint(address, function(point){
                if (point) {
                    var p = new BMap.Point(point.lng, point.lat);
                    var marker = new BMap.Marker(p);  // 创建标注
                    map.addOverlay(marker);              // 将标注添加到地图中
                    setTimeout(function(){
                        map.centerAndZoom(p, 15);
                    },1000);
                    map.setZoom(14);
                    var sContent =
                        "<h4 style='margin:0 0 5px 0;padding:0.2em 0'>"+city+"</h4>" +
                        "<p style='margin:0;line-height:1.5;font-size:13px;text-indent:2em'>"+address+"</p>" +
                        "</div>";
                    var infoWindow = new BMap.InfoWindow(sContent);  // 创建信息窗口对象
                    //图片加载完毕重绘infowindow
                    marker.openInfoWindow(infoWindow);
                }
            }, city);

        });

    });
}

//获取公司分页列表内容
function getTabList(page,tab,box){
    var unique       = $("#unique").val();
    var companyname  = $("#companyname").val();
    //var companyname = encodeURIComponent(companyname);
    //var url = INDEX_URL+"company_getinfos?"+"unique="+unique+"&companyname="+companyname+"&p="+page+"&tab="+tab+"&box="+box;
    var url = INDEX_URL+"company_getinfos";
    var ajaxData = {'unique':unique,'companyname':companyname,'p':page,'tab':tab,'box':box};
    var optionArr = [];
    var hiddenName = '';
    var hiddenValue = '';
    switch(box){
        case 'shangbiao':
            optionArr = ['sbappdateyear','sbstatus','sbflowno','sbintcls'];
            break;
        case 'zhuanli':
            optionArr = ['zlpublicationyear','zlipclist','zlkindcode','zllegalstatus'];
            break;
        default :
            break;
    }
    for(var i=0;i<optionArr.length;i++){
        hiddenName = optionArr[i];
        hiddenValue = $("input[name=" + hiddenName + "]").val();
        ajaxData[hiddenName] = hiddenValue;
    }
    $.ajax({
        type:'GET',
        dataType:"html",
        url:url,
        data:ajaxData,
        success:function(data){
            if(data){
                var tabBox = '#' + box + 'list';
                $(tabBox).html(data);
                $.scrollTo(tabBox,100);
            }
        }
    })
}

//获取公司分页列表内容(筛选条件)
function getTabListNew(ajaxData){
    var url = INDEX_URL+"company_getinfos";
    $.ajax({
        type:'GET',
        dataType:"html",
        url:url,
        data:ajaxData,
        success:function(data){
            if(data){
                var tabBox = '#' + ajaxData['box'] + 'list';
                $(tabBox).html(data);
                //$.scrollTo(tabBox,100);
            }
        }
    })
}

function boxScroll(tabBox){
    //var offsetHight = $('#company-nav').parent().height()*2;
    //$.scrollTo(tabBox,100,{ offset:{ top: -offsetHight} });
    $.scrollTo(tabBox,100);
}

//根据年度筛选财务信息
function financeYearChoose(obj) {
    var companykey = $("#unique").val();
    var companyname = $("#companyname").val();
    var box = $(obj).attr('data-option');
    var year = $(obj).attr('data-value');
    $.ajax({
        type: 'GET',
        dataType: "html",
        url: INDEX_URL + "company_getinfos",
        data: {unique:companykey,companyname:companyname,tab:'finance',box:box,year:year},
        success: function (data) {
            if (data) {
                var tabBox = '#' + box + 'list';
                var tabBoxHeader = '#' + box + 'Header';
                var text = year == '0' ? '最近数据' : year + '年度';
                var offsetHight = $(window).scrollTop() >= 200 ? $('#company-nav').height()*2 : $('#company-nav').height()*4;
                $(tabBox).html(data);
                $(obj).parent().parent().prev().find('span').first().text(text);
                $.scrollTo(tabBoxHeader,100,{ offset:{ top: -offsetHight} });
            }
        }
    })
}

//委托联系
$('.delegationSubmit').on('click',function(){
    var content = $.trim($(".delegationContent").val());
    var email = $.trim($(".delegationEmail").val());
    var phone = $.trim($(".delegationPhone").val());
    var companykey = $(".delegationCompanykey").val();
    var phoneRegExp = /^15[^4]{1}\d{8}$|^17[0,6,7,8]{1}\d{8}$|^18[\d]{9}$/;
    if(content==""){
        faldia({content:"请输入内容！"});
        return false;
    }
    if(phone==""){
        faldia({content:"请输入手机号码！"});
        return false;
    }
    if(email==""){
        faldia({content:"请输入电子邮箱！"});
        return false;
    }
    if (!phoneRegExp.test(phone)) {
        faldia({content:"手机号码不正确！"});
        return false;
    }
    if(!email.match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)) {
        faldia({content:"邮箱格式不正确！"});
        return false;
    }
    $.ajax({
        type: 'POST',
        url:INDEX_URL+'/user_contactCompany',
        data:{companykey:companykey,content:content,phone:phone,email:email},
        success: function(result){
            if(result.success){
                sucdia({content:"提交成功！"});
                $(".delegationContent").val('');
                $(".delegationEmail").val('');
                $(".delegationPhone").val('');
                window.location.reload();
            }else{
                faldia({content:"提交失败！"});
            }
        }
    });
});

//写笔记
$('.noteSubmit').on('click',function(){
    var content = $.trim($(".noteContent").val());
    var companykey = $(".noteCompanykey").val();
    var companyname = $(".noteCompanyname").val();
    if(content==""){
        faldia({content:"请输入内容！"});
        return false;
    }
    $.ajax({
        type: 'POST',
        url:INDEX_URL+'/user_writeNote',
        data:{companykey:companykey,companyname:companyname,content:content},
        success: function(result){
            if(result.success){
                sucdia({content:"提交成功！"});
                $(".noteContent").val('');
                window.location.reload();
            }else{
                faldia({content:"提交失败！"});
            }
        }
    });
});

//删除笔记
function delNote(id) {
    var companykey = $(".noteCompanykey").val();
    $.ajax({
        type: 'POST',
        url: INDEX_URL + '/user_delNote',
        data: {companykey: companykey,id:id},
        success: function (result) {
            if (result.success) {
                sucdia({content: "删除成功！"});
                window.location.reload();
            } else {
                faldia({content: "删除失败！"});
            }
        }
    });
}

function managerInfo(){
    var p = arguments[0];
    var infokind = arguments[1];
    var tab = arguments[2];
    var tabObj = '#' + tab + 'List';
    var companykey = $("input[name='managerInfoCompanykey']").val();
    var companyname = $("input[name='managerInfoCompanyname']").val();
    var name = $("input[name='managerInfoName']").val();
    $.ajax({
        url: INDEX_URL + '/company_managerInfoStatus',
        type: 'post',
        data:{companykey:companykey,companyname:companyname,name:name,infokind:infokind,tab:tab,p:p},
        dataType:'html',
        success: function (result) {
            console.log(result);
            if(result){
                $(tabObj).html(result);
            }
        }
    });
}

function payInfo(){
    var p = arguments[0];
    var infokind = arguments[1];
    var ajax = arguments[2];
    var ajaxObj = '#' + ajax + 'List';
    var companykey = $("input[name='hiddenKey']").val();
    var companyname = $("input[name='hiddenName']").val();
    $.ajax({
        url: INDEX_URL + '/company_getinfos',
        type: 'get',
        data:{tab:'pay',infokind:infokind,ajax:ajax,unique:companykey,companyname:companyname,p:p},
        dataType:'html',
        success: function (result) {
            console.log(result);
            if(result){
                $(ajaxObj).html(result);
            }
        }
    });
}

function addRadar(obj,companykey,flag){
    $.get('/radar_addOrRemove',{companykey:companykey,flag:flag},function(result){
        if(result.success){
            if(flag){//添加
                $(obj).attr('onclick','addRadar(this,"' + companykey + '",' + false + ');');
                $(obj).removeClass('btn-default');
                $(obj).addClass('btn-primary');
                $(obj).find('i').removeClass('fa-plus');
                $(obj).find('i').addClass('fa-check');
                $(obj).find('span').text('已监控');
            }else{
                $(obj).attr('onclick','addRadar(this,"' + companykey + '",' + true + ');');
                $(obj).removeClass('btn-primary');
                $(obj).addClass('btn-default');
                $(obj).find('i').removeClass('fa-check');
                $(obj).find('i').addClass('fa-plus');
                $(obj).find('span').text('监控');
            }
            sucdia({content:"操作成功"});
        }else{
            faldia({content:"操作失败:"+result.msg});
        }
    });
}



