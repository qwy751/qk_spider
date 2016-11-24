# -*- coding: utf-8 -*-
from unittest import TestCase
from app.datasource.pengyuan.transform import *
import json


def convert_obj(obj, *complex_name):
    convert = {}
    for name, value in obj.__dict__.items():
        if value is None:
            continue
        if name[0] is not '_' and name is not 'person_id' \
                and name is not 'bank_id' and name is not 'id':
            convert[name] = value
    for item in complex_name:
        complex_classes = getattr(obj, item)
        complex_list = []
        for temp in complex_classes:
            if item is 'bank_card':
                complex_list.append(convert_obj(temp, 'records'))
            else:
                complex_list.append(convert_obj(temp))
        convert[item] = complex_list
    return convert


class TestPyTransform(TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_process_person_id_risk(self):
        xmlstr = """
        <?xml version="1.0" encoding="GBK"?>
<!-- 1..1 -->
<cisReports batNo="查询批次号" unitName="查询单位名称" subOrgan="分支机构名称" queryUserID="查询操作员登录名" queryCount="查询请求数量" receiveTime="查询申请时间,格式YYYYMMDD HH24:mm:ss">
	<!-- 以下为每个查询申请的查询结果 1..n -->
	<cisReport reportID="报告编号" buildEndTime="报告生成结束时间,格式YYYY-MM-DD HH24:mm:ss" queryReasonID="查询原因ID，详见数据字典" subReportTypes="查询的收费子报告ID,多个收费子报告ID用逗号分隔" treatResult="对应的收费子报告收费次数,与subReportTypes一一对应,为大于等于0的值的集合,用逗号分隔" refID="引用ID,为查询申请条件中的引用ID" hasSystemError="有否系统错误，true：有错误，false：无错误" isFrozen="该客户是否被冻结，true：被冻结，false：未被冻结">
		<!-- 查询条件信息 1..1 -->
		<queryConditions>
			<!-- 1..n -->
			<item>
				<name>查询条件英文名称</name>
				<caption>查询条件中文名称</caption>
				<value>查询条件值</value>
			</item>
		</queryConditions>

		<!-- 个人身份认证信息 0..1 -->
		<policeCheck2Info subReportType="10603" subReportTypeCost="10604" treatResult="子报告查询状态,1：查得，2：未查得，3：其他原因未查得" treatErrorCode="treatResult=3时的错误代码,详见数据字典,treatResult!=3时,该属性不存在" errorMessage="treatResult=3时的错误描述信息,treatResult!=3时,该属性的值为空">
			 <!--0..1-->
       <item>
				<name>张三</name>
				<documentNo>123456789012345678</documentNo>
				<result>姓名和公民身份号码一致</result>
				<photo>被查询人办理身份证时的照片,jpg格式并经过Base64编码。</photo>
			</item>

		</policeCheck2Info>
		<!-- 个人风险统计信息 0..1 -->
		<personRiskStatInfo subReportType="14200" subReportTypeCost="14200" treatResult="子报告查询状态,1：查得，2：未查得，3：其他原因未查得" treatErrorCode="treatResult=3时的错误代码,详见数据字典,treatResult!=3时,该属性不存在" errorMessage="treatResult=3时的错误描述信息,treatResult!=3时,该属性的值为空">
			<!-- 0..1-->
			<stat>
				<alCount>1</alCount>
				<zxCount>2</zxCount>
				<sxCount>0</sxCount>
				<swCount>1</swCount>
				<cqggCount>2</cqggCount>
				<wdyqCount>1</wdyqCount>
			</stat>
		</personRiskStatInfo>
	</cisReport>
</cisReports>
        """
        process_person_id_risk('123456789012345678', xmlstr, db.session)
        p = Person.query.filter_by(name="张三").first()
        d = convert_obj(p, 'person_risk')
        print(json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True))

    def test_process_person_query_last_two_year(self):
        xmlstr = """
<?xml version="1.0" encoding="GBK"?>
<!-- 1..1 -->
<cisReports batNo="查询批次号" unitName="查询单位名称" subOrgan="分支机构名称" queryUserID="查询操作员登录名" queryCount="查询请求数量" receiveTime="查询申请时间,格式YYYYMMDD HH24:mm:ss">
	<!-- 以下为每个查询申请的查询结果 1..n -->
	<cisReport reportID="报告编号" buildEndTime="报告生成结束时间,格式YYYY-MM-DD HH24:mm:ss" queryReasonID="查询原因ID，详见数据字典" subReportTypes="查询的收费子报告ID,多个收费子报告ID用逗号分隔" treatResult="对应的收费子报告收费次数,与subReportTypes一一对应,为大于等于0的值的集合,用逗号分隔" refID="引用ID,为查询申请条件中的引用ID" hasSystemError="有否系统错误，true：有错误，false：无错误" isFrozen="该客户是否被冻结，true：被冻结，false：未被冻结">
		<!-- 查询条件信息 1..1 -->
		<queryConditions>
			<!-- 1..n -->
			<item>
				<name>查询条件英文名称</name>
				<caption>查询条件中文名称</caption>
				<value>查询条件值</value>
			</item>
		</queryConditions>
<historyQueryInfo subReportType="子报告ID" subReportTypeCost="收费子报告ID" treatResult="子报告查询状态,1：查得，2：未查得，3：其他原因未查得" treatErrorCode="treatResult=3时的错误代码,详见数据字典,treatResult!=3时,该属性不存在" errorMessage="treatResult=3时的错误描述信息,treatResult!=3时,该属性的值为空">
	<!-- 0..n -->
	<item>
		<unitID>单位ID。查询单位非本单位时，返回-1</unitID>
		<unit>单位名称。查询单位非本单位时，返回*****</unit>
		<unitMemberID>查询机构类型ID</unitMemberID>
		<unitMember>查询机构类型名称</unitMember>
		<queryDate>查询日期。格式为：yyyy年mm月dd日</queryDate>
	</item>
	<item>
		<unitID>单位ID。查询单位非本单位时，返回-1</unitID>
		<unit>单位名称。查询单位非本单位时，返回*****</unit>
		<unitMemberID>查询机构类型ID</unitMemberID>
		<unitMember>查询机构类型名称</unitMember>
		<queryDate>查询日期。格式为：yyyy年mm月dd日</queryDate>
	</item>
</historyQueryInfo>
	</cisReport>
</cisReports>"""
        process_person_query_last_two_years('123456789012345678', xmlstr)
        p = Person.query.filter_by(name="张三").first()
        d = convert_obj(p, 'person_queried')
        print(json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True))
