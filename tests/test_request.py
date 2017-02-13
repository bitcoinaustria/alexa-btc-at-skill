# -*- coding: utf-8 -*-
from nose.tools import *
import mock
from .fixtures.requests import TEST_FULL_REQUEST_DICT
from lambda_function import lambda_handler

class TestStandardRequest(object):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('lambda_function.get_btc_price')
    def test_response_price_value(self, get_btc_price):
        get_btc_price.return_value = 12

        request_value = TEST_FULL_REQUEST_DICT
        r = lambda_handler(request_value, [])

        assert_true("12" in r['response']['card']['content'])
        assert_true("12" in r['response']['outputSpeech']['text'])

    @mock.patch('lambda_function.get_btc_price')
    def test_response_currency(self, get_btc_price):
        get_btc_price.return_value = 12

        request_value = TEST_FULL_REQUEST_DICT
        request_value['request']['intent']['slots']['currency']['value'] = 'dollar'
        r = lambda_handler(request_value, [])

        assert_true("USD" in r['response']['card']['content'])
        assert_true("USD" in r['response']['outputSpeech']['text'])