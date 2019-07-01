# fundata-python-sdk

api.varena.com Python SDK

## 说明
- SDK 支持的 Python 版本:
    - python2.7
    - python3 (由[codeway3](https://github.com/codeway3)提供支持)
- 文档地址: http://open.varena.com/


## 使用

- 初始化 client
    ```python
    from fundata.client import init_api_client
    
    init_api_client('public_key', 'secert_key')
    ```

    初始化时，需要设置 `public_key` `secert_key`，可以在 **http://open.varena.com/** 上申请 API key，通过后，会收到邮件回复获取到对应的 key

- 调用某个接口
    ```python
    from fundata.client import get_api_client

    client = get_api_client()
    uri = '/fundata-dota2-free/v2/match/basic-info'
    data = {"match_id": 3765833999}
    res = client.api(uri, data)

    # 增加对 res 的处理
    # 请求失败时，res 返回的是 False
    # 如果是解析响应失败，则会返回 {"retcode": -1, message:"xxx" } 的数据
    # 正常的响应一般是 { "retcode": 200, "message": "", "data": {} } }
    # 一般是先判断 res 是不是 False，然后判断返回对象的 recode 是否为 200
    ```

## 实现的 API 调用
- dota2
    - match
        - single
        - batch 
            - [x] `/data-service/dota2/public/batch/match/basic_info` -> fundata.dota2.match.batch.get_batch_basic_info

