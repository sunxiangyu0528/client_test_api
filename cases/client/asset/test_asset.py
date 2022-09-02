import requests
import pytest

HOST = "https://test-api.liquiditytech.com"
headers = {"content-type": "application/json"}


class Test_Asset():

    def test_account_future(self):
        """
        合约账户信息汇总
        :return:
        """
        url = HOST + '/client/user/asset/account/future?accountId=12345'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_account_future_list(self):
        """
        合约账户资产列表
        :return:
        """
        url = HOST + '/client/user/asset/account/future/list'
        params = {
            "accountId": "12345",
            "page": 1,
            "pageSize": 5,
            "type": "funture"
        }
        res = requests.request(method="GET", url=url, headers=headers, params=params)
        print(res.json())
        assert res.status_code == 200

    def test_account_margin(self):
        """
        杠杆账户信息汇总
        :return:
        """
        url = HOST + '/client/user/asset/account/margin?accountId=12345'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_account_margin_list(self):
        """
        杠杆账户列表
        :return:
        """
        url = HOST + '/client/user/asset/account/margin/list'
        params = {
            "accountId": "12345",
            "coin": "BTC",
            "page": 1,
            "pageSize": 5,
            "type": "margin"
        }
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_account_spot(self):
        """
        现货账户总资产
        :return:
        """
        url = HOST + '/client/user/asset/account/spot?accountId=12345'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_account_spot_list(self):
        """
        现货账户列表
        :return:
        """
        url = HOST + '/client/user/asset/account/spot/list'
        params = {"accountId": "12345", "page": 1, "pageSize": 5}
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_asset_info(self):
        """
        总资产信息
        :return:
        """
        url = HOST + '/client/user/asset/info'
        res = requests.request(method="GET", url=url, headers=headers)
        print(res.json())
        assert res.status_code == 200

    def test_asset_list(self):
        """
        交易账户列表
        :return:
        """
        url = HOST + '/client/user/asset/info'
        params = {"accountZ": "12345", "exchange": "OKX", "page": 1, "pageSize": 5}
        res = requests.request(method="GET", url=url, params=params, headers=headers)
        print(res.json())
        assert res.status_code == 200


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
