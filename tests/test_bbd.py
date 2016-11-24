from unittest import TestCase

import sys

sys.path.append('..')

# -*- coding: utf-8 -*-
from app.datasource.bbd.bbd import BBD


class TestBBD(TestCase):
    def test_query(self):
        params = {'enterprise_name': u'乾康（上海）金融信息服务股份有限公司'}
        result, _ = BBD.query(**params)
        pass

    def test_query_qyxx_jbxx(self):
        result = BBD.query_qyxx_jbxx(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_qyxx_gdxx(self):
        result = BBD.query_qyxx_gdxx(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_qyxx_baxx(self):
        result = BBD.query_qyxx_baxx(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_qyxx_fzjg_extend(self):
        result = BBD.query_qyxx_fzjg_extend(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_qyxx_bgxx(self):
        result = BBD.query_qyxx_bgxx(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_qyxx_nb(self):
        result = BBD.query_qyxx_nb(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_rel(self):
        result = BBD.query_rel(company=u'乾康（上海）金融信息服务股份有限公司')
        print(result.text)
        assert result.text

    def test_query_dishonesty(self):
       result = BBD.query_dishonesty(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_zhixing(self):
       result = BBD.query_zhixing(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_ktgg(self):
       result = BBD.query_ktgg(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_zgcpwsw(self):
       result = BBD.query_zgcpwsw(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_rmfygg(self):
       result = BBD.query_rmfygg(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_qyxg_qyqs(self):
       result = BBD.query_qyxg_qyqs(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_ent_trademark(self):
       result = BBD.query_ent_trademark(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_domain_name_website_info(self):
       result = BBD.query_domain_name_website_info(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_patent(self):
       result = BBD.query_patent(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_qyxg_jyyc(self):
       result = BBD.query_qyxg_jyyc(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_ent_softw_copyr(self):
       result = BBD.query_ent_softw_copyr(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_ent_copyrights(self):
       result = BBD.query_ent_copyrights(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_ent_admin_pena(self):
       result = BBD.query_ent_admin_pena(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_recruit(self):
       result = BBD.query_recruit(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_bidinviting(self):
       result = BBD.query_bidinviting(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_bidwinner(self):
       result = BBD.query_bidwinner(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_overseasinv(self):
       result = BBD.query_overseasinv(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_licence_mining(self):
       result = BBD.query_licence_mining(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_licence_pros(self):
       result = BBD.query_licence_pros(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_qua_comm_cons(self):
       result = BBD.query_qua_comm_cons(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_licence_bui_cons(self):
       result = BBD.query_licence_bui_cons(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_qyxx_gcjljz(self):
       result = BBD.query_qyxx_gcjljz(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_qua_itsys_sup(self):
       result = BBD.query_qua_itsys_sup(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_cert_soft_ent_pro(self):
       result = BBD.query_cert_soft_ent_pro(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_licence_ind_pro(self):
       result = BBD.query_licence_ind_pro(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_qua_pes_pro(self):
       result = BBD.query_qua_pes_pro(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_licence_food_pro(self):
       result = BBD.query_licence_food_pro(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_licence_medi_pro(self):
       result = BBD.query_licence_medi_pro(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_licence_medi_oper(self):
       result = BBD.query_licence_medi_oper(company=u'乾康（上海）金融信息服务股份有限公司', page_size='10')
       print(result.text)
       assert result.text

    def test_query_qua_cos_pro(self):
       result = BBD.query_qua_cos_pro(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

    def test_query_gmp_auth(self):
       result = BBD.query_gmp_auth(company=u'乾康（上海）金融信息服务股份有限公司')
       print(result.text)
       assert result.text

if __name__ == '__main__':
    t = TestBBD()
    # t.test_query_qyxx_jbxx()
    # t.test_query_qyxx_gdxx()
    # t.test_query_qyxx_baxx()
    # t.test_query_qyxx_fzjg_extend()
    # t.test_query_qyxx_bgxx()
    # t.test_query_qyxx_nb()
    # t.test_query_rel()
    # t.test_query_dishonesty()
    # t.test_query_zhixing()
    # t.test_query_ktgg()
    # t.test_query_zgcpwsw()
    # t.test_query_rmfygg()
    # t.test_query_qyxg_qyqs()
    # t.test_query_ent_trademark()
    # t.test_query_domain_name_website_info()
    # t.test_query_patent()
    # t.test_query_qyxg_jyyc()
    # t.test_query_ent_softw_copyr()
    # t.test_query_ent_copyrights()
    # t.test_query_ent_admin_pena()
    # t.test_query_recruit()
    # t.test_query_bidinviting()
    # t.test_query_bidwinner()
    # t.test_query_overseasinv()
    # t.test_query_licence_mining()
    # t.test_query_licence_pros()
    # t.test_query_qua_comm_cons()
    # t.test_query_licence_bui_cons()
    # t.test_query_qyxx_gcjljz()
    # t.test_query_qua_itsys_sup()
    # t.test_query_cert_soft_ent_pro()
    # t.test_query_licence_ind_pro()
    # t.test_query_qua_pes_pro()
    # t.test_query_licence_food_pro()
    # t.test_query_licence_medi_pro()
    # t.test_query_licence_medi_oper()
    # t.test_query_qua_cos_pro()
    # t.test_query_gmp_auth()