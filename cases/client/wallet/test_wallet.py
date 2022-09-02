import json
import pytest
import requests

HOST = 'https://test-api.liquiditytech.com'
headers = {"content-type": "application/json"}


class Test_Wallet():

    def test_login(self):
        """
        登录获取鉴权
        :return:
        """
        url = HOST + '/user/login'
        data = {"email": "leo@liquiditytp.com", "password": "ltp123.."}
        res = requests.request(method="POST", url=url, headers=headers, data=json.dumps(data))
        print(res.json())
        headers["token"] = res.json()['data']

    def test_transfer_available(self):
        """
        查询划转可用额度
        :return:
        """
        url = HOST + '/client/transfer/account/available'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_transfer_apply(self):
        """
        发起划转请求
        :return:
        """
        url = HOST + '/client/transfer/apply'
        data = {
            "accountType": "string",
            "amount": 0,
            "coin": "string",
            "fromAccountId": 0,
            "fromExchange": "string",
            "toAccountId": 0,
            "toExchange": "string",
            "transferType": "string"
        }
        res = requests.request(method="POST", url=url, headers=headers, data=json.dumps(data))
        print(res.json())
        assert res.status_code == 200

    def test_transfer_list(self):
        """
        划转记录列表
        :return:
        """
        url = HOST + '/client/transfer/list'
        params = {
            "from": "str",
            "coin": "BTC",
            "page": 1,
            "pageSize": 5,
            "to": "str"
        }
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_withdraw(self):
        """
        发起出金申请
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw'
        data = {
            "accountId": 0,
            "address": "string",
            "addressTag": "string",
            "amount": 0,
            "clientOrderId": "string",
            "currency": "string",
            "ltpUserId": 0,
            "network": "string"
        }
        res = requests.request(method="POST", url=url, headers=headers, data=json.dumps(data))
        print(res.json())

    def test_withdraw_list(self):
        """
        出金记录列表
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw/list'
        params = {
            "accountId": 123456,
            "currency": "BTC",
            "page": 1,
            "pageSize": 5
        }
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_withdraw_ifwhiteuser(self):
        """
        白名单用户
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw/ifWhiteUser'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_deposit_withdraw(self):
        """
        出入金列表
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/info'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_address_create(self):
        """
        新增出金地址
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw/address/create'
        params = {
            "address": "",
            "addressTag": "",
            "currency": "BTC",
            "ltpUserId": "",
            "network": ""
        }
        res = requests.request(method="POST", url=url, headers=headers, params=params)
        print(res.json())
        assert res.status_code == 200

    def test_delete_address(self):
        """
        删除出金地址
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw/address/1'
        res = requests.request(method="DELETE", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_withdraw_address(self):
        """
        出金地址列表
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/withdraw/address'
        params = {"currency": "BTC", "page": 1, "pageSize": 5}
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_deposit_address(self):
        """
        入金地址生成
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/deposit/address?userDepositAddressRequest=string'
        res = requests.request(method='GET', url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_deposit_list(self):
        """
        入金列表
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/deposit/list'
        params = {
            "page": 1, "pageSize": 5, "accountId": "12345", "currency": "BTC"
        }
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_deposit_recent(self):
        """
        默认上一次入金账号查询
        :return:
        """
        url = HOST + '/client/user/depositAndWithdraw/deposit/recent'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
