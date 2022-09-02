import json

import requests
headers = {"content-type": "application/json"}


def test_login():
    """
    登录获取鉴权
    :return:
    """
    url = '/user/login'
    data = {"email": "leo@liquiditytp.com", "password": "ltp123..."}
    res = requests.request(method="POST", url=url, headers=headers, data=json.dumps(data))
    print(res.json())

if __name__ == '__main__':
    test_login()