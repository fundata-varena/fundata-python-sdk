#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import hashlib
import json
import urllib
import logging
import time
import random
import string
import urlparse
import requests

DEFAULT_API_SERVER = 'http://api.varena.com'

_logger = logging
logging.getLogger().setLevel("INFO")


class FundataApiException(Exception):
    """ 用于表示异常请求异常
    """
    def __str__(self):
        return "varena API request Error"


# Refer from:
# 1. https://pythontips.com/2013/07/28/generating-a-random-string/
# 2. https://stackoverflow.com/a/2257449
def _random_str(count):
    """返回指定长度的随机字符串
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(count)])


def _urlencode(param):
    try:
        return urllib.urlencode(param)
    except AttributeError:
        return urllib.parse.urlencode(param)


def val_to_str(val):
    """ 把参数的值转换成字符串
    """
    if type(val) == bool:
        return 'true' if val is True else 'false'

    if type(val) != list:
        return str(val)

    # FIXME, how to handle list or nest object?

    val_arr = [val_to_str(item_val) for item_val in val]
    return ','.join(val_arr)


def generate_sign(nonce, secret_key, api_time, uri, params):
    """根据待签名的参数和 secret_key 来生成签名
    """
    # 参数排序
    items = sorted(params.items())

    # 组装待签名的参数
    str_arr = ['{0}={1}'.format(str(key), val_to_str(val)) for key, val in items]
    params_str = '&'.join(str_arr)

    to_sign_str = '|'.join([nonce, secret_key, '{0}'.format(api_time), uri, params_str])

    # 使用 md5 计算 hash
    hash_gen = hashlib.md5()
    hash_gen.update(to_sign_str.encode('utf-8'))
    hash_value = hash_gen.hexdigest()

    return hash_value


class InternalRequest(object):
    def __init__(self, base_url, timeout):
        self._base_url = base_url

    def get(self, uri, params, headers):
        headers['Content-Type'] = 'application/json; charset=utf-8'

        tmp_params = {}
        for key, val in params.items():
            tmp_params[key] = val_to_str(val)

        query = '{0}?{1}'.format(uri, _urlencode(tmp_params))
        url = '{0}{1}'.format(self._base_url, query)

        _logger.debug('Get %s with api-nonce %s', url, headers.get('Accept-ApiNonce'))

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            _logger.exception('GET request error %s', uri)
            raise Exception(e)

    def post(self, uri, params, headers):
        body = json.dumps(params)
        headers['Content-Type'] = 'application/json; charset=utf-8'

        url = '{0}{1}'.format(self._base_url, uri)
        _logger.debug('Post %s %s with api-nonce %s', uri, body, headers.get('Accept-ApiNonce'))

        try:
            response = requests.post(url, json=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            _logger.exception('POST request error %s', url)
            raise Exception(e)


class ApiClient(object):
    api_server = DEFAULT_API_SERVER

    def __init__(self, public_key, secret_key, timeout=20):
        if not public_key or not secret_key:
            raise FundataApiException('No public key or secret key provided')

        self._public_key = public_key
        self._secret_key = secret_key
        self._request = InternalRequest(ApiClient.api_server, timeout)

    @classmethod
    def configure(cls, api_server):
        cls.api_server = api_server if api_server else DEFAULT_API_SERVER

    def api(self, uri, data, options=None, method='GET'):
        parse_result = urlparse.urlparse(uri)
        _uri_path = parse_result.path
        params = dict({}, **data)
        if parse_result.query:
            params.update(urlparse.parse_qs(parse_result.query))

        nonce = _random_str(10)  # 默认长度为10
        if options and options.get('nonce', False):
            nonce = options['nonce']
        api_time = int(time.time())

        sign = generate_sign(nonce, self._secret_key, api_time, _uri_path, params)

        headers = {
            'Accept-ApiKey': self._public_key,
            'Accept-ApiNonce': nonce,
            'Accept-ApiTime': '{0}'.format(api_time),
            'Accept-ApiSign': sign,
        }

        _logger.info("Request uri: %s, params: %s, headers: %s", _uri_path, params, headers)

        if method == 'POST':
            return self._request.post(_uri_path, params, headers)
        elif method == 'GET':
            return self._request.get(_uri_path, params, headers)
        else:
            raise FundataApiException('Only POST or GET is supported')
