# -*- coding: utf-8 -*-
import time
from nose.tools import ok_
from iamport import Iamport


class TestIamport(object):
    def setUp(self):
        imp_key = '5779563289182967'
        imp_secret = 'Bsxzv294KW1iDoxrnHjAHWlvLCDpu1E6ubFZeP4YL5gouNQRv9sc5OIRqmgVnU1R6GRkvVjh0zGvnwmS'
        self.iamport = Iamport(imp_key, imp_secret)
        self.merchant_uid = 'iamport_merchant_test_%d' % int(time.time())
        self.customer_uid = 'iamport_customer_test_%d' % int(time.time())

    def tearDown(self):
        pass

    def test_one_time_failure(self):
        ''' 즉시 결제 '''
        try:
            rv = self.iamport.onetime(self.merchant_uid, '9446-0380-1234-1234',
                                      '2022-01', '971225', '97', '1004')
        except self.iamport.IamportError as e:
            ok_(e.code == -1, e)
            err_msg = u'카드정보 인증에 실패하였습니다. [F113]거래거절 카드번호틀림'
            ok_(e.message == err_msg, e)

    def test_cancel_failure(self):
        ''' 전액 취소 '''
        try:
            self.iamport.cancel(self.customer_uid, 1004)
        except self.iamport.IamportError, e:
            ok_(e.code == 1, e)
            ok_(e.message == u'취소할 결제건이 존재하지 않습니다.', e)

    def test_cancel_failure_1(self):
        ''' 부분 취소 '''
        try:
            self.iamport.cancel(self.customer_uid, 500)
        except self.iamport.IamportError, e:
            ok_(e.code == 1, e)
            ok_(e.message == u'취소할 결제건이 존재하지 않습니다.', e)

    def test_find_failure(self):
        ''' 주문 정보 가져오기 '''
        try:
            self.iamport.find(self.merchant_uid)
        except self.iamport.IamportError, e:
            ok_(e.code == -1, e)
            ok_(e.message == u'존재하지 않는 결제정보입니다.', e)

    def test_find_by_uid_failure(self):
        ''' imp_uid로 주문 정보 가져오기 '''
        try:
            self.iamport.find_by_uid('iamport_uid')
        except self.iamport.IamportError, e:
            ok_(e.code == -1, e)
            ok_(e.message == u'존재하지 않는 결제정보입니다.', e)

    def test_schedule_failure(self):
        ''' 스케줄 등록 '''
        try:
            self.iamport.schedule(self.customer_uid, self.merchant_uid,
                                  '9446-0380-1234-1234', '2022-01',
                                  '971225', '97', 1004)
        except self.iamport.IamportError, e:
            ok_(e.code == 1, e)
            err_msg = u'카드정보 확인에 실패하였습니다. [F113]거래거절 카드번호틀림'
            ok_(e.message == err_msg, e.message)

    def test_unschedule_failure(self):
        ''' 스케줄 취소 '''
        try:
            self.iamport.unschedule(self.customer_uid, 'iamport_test_1')
        except self.iamport.IamportError, e:
            ok_(e.code == 1, e)
            ok_(e.message == u'취소할 예약결제 기록이 존재하지 않습니다.', e)

    def test_again_failure(self):
        ''' 재결제 '''
        try:
            self.iamport.again(self.customer_uid, self.merchant_uid, 1004)
        except self.iamport.IamportError, e:
            ok_(e.code == 1, e.message)
            ok_(e.message == u'등록되지 않은 구매자입니다.', e)
