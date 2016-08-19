# -*- coding: utf-8 -*-
import time
import requests
from datetime import datetime, timedelta
from urllib2 import quote

__all__ = ['Iamport', 'IAMPORT_URL', '__version__']
__version__ = '0.0.1'

IAMPORT_URL = 'https://api.iamport.kr'


class Iamport(object):
    def __init__(self, imp_key=None, imp_secret=None, imp_url=IAMPORT_URL):
        self.imp_key = imp_key
        self.imp_secret = imp_secret
        self.imp_url = imp_url
        self.req = requests.session()

    class IamportError(Exception):
        def __init__(self, code=None, message=None, *args):
            self.code = code
            self.message = message
            super(Exception, self).__init__(message, code, *args)

    def set_config(self, imp_key, imp_secret):
        self.imp_key = imp_key
        self.imp_secret = imp_secret

    def _generate_response(self, response):
        result = response.json()
        if result['code'] != 0:
            raise self.IamportError(result.get('code'), result.get('message'))
        elif ('response' in result and
              isinstance(result['response'], dict) and
              result['response'].get('fail_reason')):
            raise self.IamportError(2, result['response'].get('fail_reason'))
        return result.get('response')

    def _generate_token(self):
        url = '%s/users/getToken' % (self.imp_url)
        payload = {'imp_key': self.imp_key, 'imp_secret': self.imp_secret}
        res = self.req.post(url, data=payload)
        return self._generate_response(res).get('access_token')

    def _generate_headers(self, headers={}):
        if not isinstance(headers, dict):
            raise self.IamportError(-1, 'Header Error')
        headers['X-ImpTokenHeader'] = self._generate_token()
        headers['user-agent'] = 'Payment-%s' % __version__
        return headers

    def _get(self, url, payload=None, headers={}):
        headers = self._generate_headers(headers)
        res = self.req.get(url, headers=headers, params=payload)
        return self._generate_response(res)

    def _post(self, url, payload=None, headers={}):
        headers = self._generate_headers(headers)
        res = self.req.post(url, headers=headers, json=payload)
        return self._generate_response(res)

    def schedule(self, customer_uid, merchant_uid, card_number,
                 expiry, birth, pwd, amount, schedule_at=None,
                 checking_amount=0):
        if isinstance(schedule_at, datetime):
            pass
        elif isinstance(schedule_at, (str, unicode)):
            schedule_at = datetime.strptime(schedule_at, '%Y-%d-%m %H:%M:%s')
        else:
            schedule_at = datetime.today() + timedelta(days=30)
        schedule_at = time.mktime(schedule_at.timetuple())
        url = '%s/subscribe/payments/schedule' % (self.imp_url)
        payload = {
            'customer_uid': customer_uid,
            'card_number': card_number,
            'expiry': expiry,
            'birth': birth,
            'pwd_2digit': pwd,
            'checking_amount': checking_amount,
            'schedules': [
                {
                    'merchant_uid': merchant_uid,
                    'schedule_at': schedule_at,
                    'amount': amount
                }
            ]
        }
        return self._post(url, payload)

    def unschedule(self, customer_uid, merchant_uid):
        url = '%s/subscribe/payments/unschedule' % (self.imp_url)
        payload = {
            'customer_uid': customer_uid,
            'merchant_uid': merchant_uid
        }
        return self._post(url, payload)

    def again(self, customer_uid, merchant_uid, amount, name=None,
              buyer_name=None, buyer_email=None, buyer_tel=None,
              buyer_addr=None, buyer_postcode=None, card_quota=None):
        url = '%s/subscribe/payments/again' % (self.imp_url)
        payload = {
            'customer_uid': customer_uid,
            'merchant_uid': merchant_uid,
            'amount': amount,
            'name': name,
            'buyer_name': buyer_name,
            'buyer_email': buyer_email,
            'buyer_tel': buyer_tel,
            'buyer_addr': buyer_addr,
            'buyer_postcode': buyer_postcode,
            'card_quota': card_quota
        }
        return self._post(url, payload)

    def onetime(self, merchant_uid, card_number, expiry,
                birth, password, amount, vat=None, customer_uid=None,
                name=None, buyer_name=None, buyer_email=None,
                buyer_tel=None, buyer_addr=None, buyer_postcode=None,
                card_quota=None):

        url = '%s//subscribe/payments/onetime' % (self.imp_url)
        payload = {
            'merchant_uid': merchant_uid,
            'amount': amount,
            'card_number': card_number,
            'expiry': expiry,
            'birth': birth,
            'pwd_2digit': password,
            'vat': vat,
            'customer_uid': customer_uid,
            'name': name,
            'buyer_name': buyer_name,
            'buyer_email': buyer_email,
            'buyer_tel': buyer_tel,
            'buyer_addr': buyer_addr,
            'buyer_postcode': buyer_postcode,
            'card_quota': card_quota
        }
        return self._post(url, payload)

    def cancel(self, merchant_uid, amount, reason=None):
        url = '%s/payments/cancel' % (self.imp_url)
        payload = {
            'merchant_uid': merchant_uid,
            'amount': amount,
            'reason': reason
        }
        return self._post(url, payload)

    def find(self, merchant_uid):
        if merchant_uid is not None:
            merchant_uid = quote(merchant_uid)
        url = '%s/payments/find/%s' % (self.imp_url, merchant_uid)
        return self._get(url)

    def find_by_uid(self, imp_uid):
        url = '%s/payments/%s' % (self.imp_url, imp_uid)
        return self._get(url)
