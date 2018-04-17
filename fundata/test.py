# -*- coding: utf-8 -*-

from pprint import pprint
from request import ApiClient


def test():
    # FIXME，需要设置
    public_key, secret_key = ('', '')

    # 用 public key，secret key 来初始化 client
    client = ApiClient(public_key, secret_key)

    # 准备 API 需要的参数
    uri = '/data-service/dota2/public/match/{0}/basic_info'.format(3765833999)
    data = {}

    res = client.api(uri, data)

    pprint(res)


if __name__ == "__main__":
    test()