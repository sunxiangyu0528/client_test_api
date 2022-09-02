import time

from exchange.trade import LTP


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

    time.sleep(2)
    assert ltp.flag

    ltp.send_subscribe(op="unsubscribe")
    time.sleep(2.5)
    assert ltp.flag is False

    ltp.send_subscribe(op="subscribe")
    time.sleep(2)
    assert ltp.flag


def test_market_okx_03():
    """
    Author: Alex
    Logic: 订阅之后，再订阅其他exchange
    Expect：？
    """

    ltp = LTP()
    ltp.on_recv()
    ltp.task_ping()
    ltp.send_subscribe(op="subscribe")

    time.sleep(1)

    ltp.send_subscribe(exchange="1000")


    while 1:
        pass


def test_market_okx_04():
    """
    Author: Alex
    Logic: 订阅之后，再订阅其他symbol
    Expect：？
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
    ltp.task_ping()
    ltp.send_subscribe(exchange="ERROR")
    ltp.send_subscribe(channel="ERROR")
    ltp.send_subscribe(op="ERROR")
    ltp.send_subscribe(symbol="ERROR")

    while 1:
        pass

def test_market_okx_05():
    """
    Author: Alex
    Logic: 多链路压测
    Expect：
    """
    for i in range(1):
        t = LTP()
        t.send_subscribe()
        t.on_recv()
        t.task_ping()
        t.task_check()

    while 1:
        pass


