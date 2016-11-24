$(function () {
    var a = {
        "msg": "ok",
        "rsize": 1,
        "total": 1,
        "results": [
            {
                "operating_period": null,
                "regno": "310104000538800",
                "company_regorg": "310000",
                "investcap_amount": null,
                "ipo_company": null,
                "company_type": "股份有限公司（非上市）",
                "approval_date": "2013-03-05",
                "create_time": "2016-08-22T09:48:51",
                "esdate": "2013-03-05",
                "realcap_amount": null,
                "credit_code": "91310104062598052B",
                "regcap": "900.000000万人民币",
                "id": 138161523,
                "enterprise_status": "存续（在营、开业、在册）",
                "invest_cap": null,
                "openfrom": "2013-03-05",
                "regorg": "上海市工商局",
                "frname": "周滨",
                "regcapcur": null,
                "parent_firm": null,
                "bbd_qyxx_id": "c76e3a2334244044843d0127a9dc3dcb",
                "company_county": "310104",
                "operate_scope": "接受金融机构委托从事金融信息技术外包，接受金融机构委托从事金融业务流程外包，接受金融机构委托从事金融知识流程外包，商务信息咨询（除经纪），电子产品、计算机软硬件（除计算机信息系统安全专用产品）、通讯设备的销售。\r\n【依法须经批准的项目，经相关部门批准后方可开展经营活动】",
                "regcap_currency": "人民币",
                "company_name": "乾康（上海）金融信息服务股份有限公司",
                "bbd_type": "shanghai",
                "company_industry": "F",
                "regno_or_creditcode": "91310104062598052B",
                "type": "上海",
                "revoke_date": null,
                "investcap_currency": null,
                "form": null,
                "bbd_history_name": "[]",
                "bbd_uptime": 1471815111,
                "bbd_dotime": "2016-08-22",
                "cancel_date": null,
                "regcap_amount": 9000000.0,
                "address": "上海市徐汇区桂箐路7号3号楼801室",
                "opento": null,
                "company_enterprise_status": "存续",
                "company_province": "上海",
                "company_currency": null,
                "realcap_currency": null,
                "realcap": null,
                "frname_id": "5c3c65eb92347d97c648feafb8664bfe",
                "frname_compid": "1",
                "company_companytype": "1220"
            }
        ],
        "err_code": 0
    }
    var data = a.results[0];
    console.log(data)

    // template.compile(source);
    // var html = render({list: ['摄影', '电影', '民谣', '旅行', '吉他']});
    //
    // var render = template.compile(source);
    // var html = render({list: ['摄影', '电影', '民谣', '旅行', '吉他']});


    var html = template('resultInfo', data);
    console.log(html)
    // document.getElementById("base_div").innerHTML = html;
})