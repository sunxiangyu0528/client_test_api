import time

import numpy
import pytest

from common.tools import Check
from common.utils import manual_step
from exchange.exchange import LTP, OKX, BN


def test_okx_01():
    """
    author: alex
    logic: 校验极速行情获取的数据和交易所获取的数据的延时
    exception: 延时
    """
    dq1 = list()
    dq2 = list()
    ltp = LTP(exchange="1001", symbol="BTC_USDT", share_dq=dq1)
    okx = OKX(symbol="BTC_USDT", share_dq=dq2)
    okx.start()
    time.sleep(1)
    ltp.start()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)

    ltp_data = dq1.pop(0)
    okx_data = dq2.pop(0)
    check = Check(ex_name="OKX")
    while True:
        if check.is_equals(ltp_data, okx_data):
            break
        okx_data = dq2.pop(0)

    times = 500
    ans = []
    while times > 0:
        if dq2 and dq1:
            res = ltp_data['data']["timestamp"] - int(okx_data['data'][0]["ts"])
            # res = (ltp_data["get_ts"] - okx_data["get_ts"]) * 1000
            ans.append(res)
            print(f"========={res}==========")
            print(f"ltp: {ltp_data}")
            print(f"okx: {okx_data}")
            print(f"=========end============")
            okx_data = dq2.pop(0)
            ltp_data = dq1.pop(0)
            times -= 1
    assert numpy.median(ans) <= 3


@pytest.mark.parametrize('n', [1])
@pytest.mark.tags("manual", "smoke")
def test_okx_02(n):
    """
    author: alex
    logic: 并发订阅，观察稳定性
    exception:
    """
    for i in range(n-1):
        LTP(exchange="1001", symbol="BTC_USDT", debug=False).start()

    LTP(exchange="1001", symbol="BTC_USDT").start()
    while True:
        pass


@pytest.mark.parametrize(['exchange', "symbol"], [("1001", "BTC_USDT"), ("1001", "ETH_USDT")])
def test_okx_03(exchange, symbol):
    """
    author：alex
    logic：校验 OKX 500组数据正确性
    """

    dq1 = list()
    dq2 = list()
    ltp = LTP(exchange=exchange, symbol=symbol, share_dq=dq1)
    okx = OKX(symbol=symbol, share_dq=dq2)
    okx.start()
    time.sleep(1)
    ltp.start()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)

    ltp_data = dq1.pop(0)
    okx_data = dq2.pop(0)
    check = Check(ex_name="OKX")
    while True:
        if check.is_equals(ltp_data, okx_data):
            break
        okx_data = dq2.pop(0)

    times = 500
    while times > 0:
        if dq2 and dq1:
            okx_data = dq2.pop(0)
            ltp_data = dq1.pop(0)
            print(f"=========start==========")
            print(f"ltp: {ltp_data}")
            print(f"okx: {okx_data}")
            print(f"=========end============")
            assert check.is_equals(ltp_data, okx_data)
            times -= 1


@pytest.mark.parametrize(['exchange', "symbol"], [("1000", "BTC_USDT"), ("1000", "ETH_USDT")])
def test_bn_01(exchange, symbol):
    """
    author: alex
    logic: 校验binance 500组数据正确性
    """

    dq1 = list()
    dq2 = list()
    ltp = LTP(exchange=exchange, symbol=symbol, share_dq=dq1, debug=False)
    ex = BN(symbol=symbol, share_dq=dq2, debug=False)
    ex.start()
    time.sleep(1)
    ltp.start()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)
    while not dq2:
        print("ex no data...")
        time.sleep(0.5)

    ltp_data = dq1.pop(0)
    ex_data = dq2.pop(0)
    check = Check(ex_name="OKX")
    while True:
        if check.is_equals(ltp_data, ex_data):
            break
        ex_data = dq2.pop(0)

    times = 500
    while times > 0:
        if dq2 and dq1:
            ex_data = dq2.pop(0)
            ltp_data = dq1.pop(0)
            # print(f"=========start==========")
            # print(f"ltp: {ltp_data}")
            # print(f"okx: {ex_data}")
            # print(f"=========end============")
            if check.is_equals(ltp_data, ex_data):
                times -= 1
            else:
                print(f"ex_data: {ex_data}")
                print(f"ltp_data: {ltp_data}")
                assert False
def test_bn_02():

    ltp = LTP(exchange="1000", symbol="BTC_USDT")
    ltp.start()
    manual_step("kkkkkkkkk")
    # ltp.send_unsubscribe()
    # ltp.send_subscribe()
    while 1:
        pass