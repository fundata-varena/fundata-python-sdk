#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from .request import FundataApiException, ApiClient

api_client = None


def get_api_client():
    """获取 api client 对象
    """
    print('get', api_client)
    if api_client is None:
        raise FundataApiException('API client is not initialized')

    return api_client


def init_api_client(public_key, api_secret, api_server=None):
    """初始化 api client
    """
    if api_server is not None:
        ApiClient.configure(api_server)

    global api_client
    api_client = ApiClient(public_key, api_secret)
    print('init', api_client)
