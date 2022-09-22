import time
from collections import deque

import pytest

from common.tools import Check
from exchange.trade import LTP, OKX, BN


def test_market_okx_01():
    """
    Author: Alex
    Logic: 订阅后，未在规定30s发送 ping 包
    Expect：服务端主动断开连接，客户端连接断开
    """

    ltp = LTP()
    ltp.send_subscribe()
    ltp.on_recv()

    time.sleep(35)

    assert ltp.ws.connected is False


def test_market_okx_02():
    """
    Author: Alex
    Logic: subscribe -> unsubscribe -> subscribe
    Expect：取消订阅后，不会存在数据推送，再次订阅，存在数据推送
    """

    ltp = LTP()
    ltp.on_recv()
    ltp.task_ping()
    ltp.send_subscribe(op="subscribe")
    ltp.task_check()

    time.sleep(1)
    assert ltp.flag

    ltp.send_subscribe(op="unsubscribe")
    time.sleep(5)
    assert ltp.flag is False

    ltp.send_subscribe(op="subscribe")
    time.sleep(2)
    assert ltp.flag


def test_market_okx_03():
    """
    Author: Alex
    Logic: 订阅之后，再订阅其他exchange
    Expect：支持多个订阅
    """

    ltp = LTP()
    ltp.on_recv()
    ltp.task_ping()
    ltp.send_subscribe()

    time.sleep(1)

    ltp.send_subscribe()
    ltp.send_subscribe()
    ltp.send_subscribe()

    while 1:
        pass


def test_market_okx_04():
    """
    Author: Alex
    Logic: 订阅之后，再订阅其他symbol
    Expect：支持多个订阅
    """

    ltp = LTP()
    ltp.on_recv()
    ltp.task_ping()
    ltp.send_subscribe(op="subscribe")

    time.sleep(1)

    ltp.send_subscribe(symbol="ETH_USDT")

    while 1:
        pass


def test_market_okx_05():
    """
    Author: Alex
    Logic: 发送错误字段
    Expect：？
    """
    ltp = LTP()
    ltp.on_recv()
    ltp.send_subscribe(exchange="ERROR")
    ltp.send_subscribe(channel="ERROR")
    ltp.send_subscribe(op="ERROR")
    ltp.send_subscribe(symbol="ERROR")

    while 1:
        pass


def test_market_okx_06():
    """
    Author: Alex
    Logic: 多链路压测
    Expect：
    """
    for i in range(0):
        t = LTP()
        t.send_subscribe(channel="bbo")
        t.on_recv()
        t.task_ping()
        # t.task_check()

    okx = OKX()
    okx.send_subscribe(channel="trades")
    okx.on_recv()

    while 1:
        pass


@pytest.mark.parametrize("symbol", ["BTC_USDT", "ETH_USDT", "ADA_USDT",
                                    "SOL_USDT", "XRP_USDT", "TRX_USDT",
                                    "DOGE_USDT", "DOT_USDT", "LTC_USDT",
                                    "ETC_USDT"])
def test_market_01(symbol):
    """
    Author: Alex
    Logic: 验证ltp - okx 不同币种的数据正确性
    Expect：符合预期
    """

    dq1 = deque()
    dq2 = deque()

    ltp = LTP(share_dq=dq1)
    ex = OKX(share_dq=dq2)

    ex.send_subscribe(instId=symbol)
    ex.on_recv()
    time.sleep(1)
    ltp.send_subscribe(symbol=symbol)
    ltp.on_recv()
    ltp.task_ping()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)
    while not dq2:
        print("ex no data...")
        time.sleep(0.5)

    ltp_data = dq1.popleft()
    ex_data = dq2.popleft()
    check = Check(ex_name="OKX")
    while True:
        if check.is_equals(ltp_data, ex_data):
            break
        ex_data = dq2.popleft()

    times = 300
    while times > 0:
        if dq2 and dq1:
            ex_data = dq2.popleft()
            ltp_data = dq1.popleft()
            print(f"=========start==========")
            print(f"ltp: {ltp_data}")
            print(f"okx: {ex_data}")
            print(f"=========end============")
            if check.is_equals(ltp_data, ex_data):
                times -= 1
            else:
                print(f"ex_data: {ex_data}")
                print(f"ltp_data: {ltp_data}")
                assert False
    ltp.flag = False
    ex.flag = False


@pytest.mark.parametrize("symbol", ["BTC_USDT", "ETH_USDT", "ADA_USDT",
                                    "SOL_USDT", "XRP_USDT", "TRX_USDT",
                                    "DOGE_USDT", "DOT_USDT", "LTC_USDT",
                                    "ETC_USDT"])
def test_market_02(symbol):
    """
    Author: Alex
    Logic: 验证ltp - okx 不同币种的数据正确性
    Expect：符合预期
    """

    dq1 = deque()
    dq2 = deque()

    ltp = LTP(share_dq=dq1)
    ex = BN(share_dq=dq2, symbol=symbol)

    ex.on_recv()
    time.sleep(1)
    ltp.send_subscribe(exchange="1000", symbol=symbol)
    ltp.on_recv()
    ltp.task_ping()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)
    while not dq2:
        print("ex no data...")
        time.sleep(0.5)

    ltp_data = dq1.popleft()
    ex_data = dq2.popleft()
    check = Check(ex_name="BN")
    while True:
        if check.is_equals(ltp_data, ex_data):
            break
        ex_data = dq2.popleft()

    times = 100
    while times > 0:
        if dq2 and dq1:
            ex_data = dq2.popleft()
            ltp_data = dq1.popleft()
            print(f"=========start==========")
            print(f"ltp: {ltp_data}")
            print(f"okx: {ex_data}")
            print(f"=========end============")
            if check.is_equals(ltp_data, ex_data):
                times -= 1
            else:
                print(f"ex_data: {ex_data}")
                print(f"ltp_data: {ltp_data}")
                assert False
    ltp.flag = False
    ex.flag = False


def test_01():
    ltp = LTP()
    ltp.send_subscribe()
    ltp.on_recv()
    ltp.task_ping()
    while True:
        pass
