# -*- coding: utf-8 -*-
import os
import sys
from pprint import pprint
from fundata.request import ApiClient
from fundata.client import init_api_client
from fundata.dota2.match import get_batch_basic_info


print(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def test(public_key, secret_key):
    # 用 public key，secret key 来初始化 client
    client = ApiClient(public_key, secret_key)

    # 准备 API 需要的参数
    uri = '/fundata-dota2-free/v2/match/basic-info'
    data = {"match_id": 3765833999}

    res = client.api(uri, data)

    pprint(res)


# 测试获取批量比赛基本数据
def test_batch_basic_info(key, sec):
    # FIXME，需要设置 public_key/secret_key
    init_api_client(key, sec)

    res = get_batch_basic_info(1522724457, 0, 2)
    pprint(res)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        pprint("usage: {} apikey sec".format(__file__))
        sys.exit(1)
    test_batch_basic_info(sys.argv[1], sys.argv[2])
