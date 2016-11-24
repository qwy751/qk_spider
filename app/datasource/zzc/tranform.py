# -*- coding: utf-8 -*-
import json
import sys
sys.path.append("..")
from ..utils.tools import convert_dict


test = """
[
        {
            "id": "a97187f0-cae2-400c-bec4-99c726ff9c44",
            "name": "段鸿煊",
            "pid": "342122198010100109",
            "mobile": "13989881734",
            "work_name": "龙源泰传媒有限责任公司",
            "work_phone": "010-14922586",
            "work_address": "天津市武汉市崔中心93号",
            "address": "天津市武汉市崔中心93号",
            "home_phone": "021-82503322",
            "home_address": "云南省上安市曹栋571号",
            "confirm_type": "fraud",
            "created_at": "2015-11-17T20:49:51+08:00",
            "updated_at": "2015-11-17T20:49:51+08:00"
        },
        {
            "id": "fc35aa05-42ea-498a-80fb-1627f1719784",
            "name": "何擎苍",
            "pid": "435122198401023856",
            "mobile": "13913622391",
            "work_name": "深圳市工贸有限公司",
            "work_address": "山西省厦林市董路9号",
            "home_address": "浙江省诸州市杜桥2号",
            "address": "天津市武汉市崔中心93号",
            "marital_status": "married",
            "loan_type": "房贷",
            "confirm_type": "reject",
            "repayment": "nn",
            "applied_at": "2015-10-19T19:51:18+08:00",
            "confirmed_at": "2014-11-26T18:35:09+08:00",
            "province": "四川省",
            "city": "长宁市",
            "contacts":[
                {
                    "name": "梁潇然",
                    "phone": "13626292036",
                    "work_name": "德金益明有限公司",
                    "relationship": "mother"
                }
            ],
            "created_at": "2015-11-17T20:49:51+08:00",
            "updated_at": "2015-11-17T20:49:51+08:00"
        }
    ]
"""


def format_result(content):
    # result_dict = json.loads(content)
    converted = convert_dict(content)
    return json.dumps(converted, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    print(format_result(test))
    