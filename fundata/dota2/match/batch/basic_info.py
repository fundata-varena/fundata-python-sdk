#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from ....client import get_api_client

BasicInfoURI = '/fundata-dota2-free/v2/match/basic-info/batch'


def get_batch_basic_info(start_time, start_from=0, limit=100):
    """批量获取比赛基本数据, 可以批量获取从一天开始(UTC时间)获取到一天结束的比赛基本数据

    `start_time` required, 比赛开始时间, 表示取从何时开始的比赛数据
    `start_from` optional, 比赛ID, 表示取从哪场比赛之后的比赛数据;
                 不为空时，start_from 与 start_time 必须具体为某一场比赛对应的数据
                 比如第一次以 start_time 获取了一个比赛列表后，列表最后的比赛对应的ID为 3813773851, 对应的比赛开始时间是1522724457，
                 则获取之后的比赛列表的方式是传 start_time=1522724457,start_from=3813773851，即可获取开始在1522724457之后并且比赛ID大于3813773851的比赛列表;
                 如此往复，知道返回的数据条目数小于 limit，然后再从新的一天的 start_time 开始
    `limit` optional, 表示返回数据的最大条目数，传零或者不传默认返回100条数据，不可超过 200，如果返回的条目数小于limit，则意味着当前的查询条件已经没有更多数据了
    """

    client = get_api_client()
    data = {
        'start_time': start_time,
    }

    if start_from > 0:
        data['start_from'] = start_from

    if limit > 0 and limit <= 200:
        data['limit'] = limit

    return client.api(BasicInfoURI, data)
