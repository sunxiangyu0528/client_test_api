import ssl
import json
from threading import Thread

from common.handle_db import DbTrade
from common.utils import get_now_time
from config import ws

import pytest
import time
import websocket
from websocket import create_connection, WebSocketConnectionClosedException

from common.log import logger
from config.ws import OKX_URL, LTP_URL, li_01, li_02
from exchange.exchange import Base, LTP, OKX

base = Base(url=LTP_URL)
db_trade = DbTrade()


class TestDemo(object):

    @pytest.mark.parametrize('symbol', li_01)
    def test_01(self, symbol):
        """
        author: Andre
        Logic : "channel": "book","exchange": "1001"的情况
        """
        data = {
            "args": {
                "exchange": "1001",
                "symbol": symbol,
                "channel": "book"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                if eval(result).get("event") == None:
                    # receiveTimestampNs = eval(result)["data"]["receiveTimestampNs"]
                    # sendTimestampNs = eval(result)["data"]["sendTimestampNs"]
                    timestamp = eval(result)["data"]["timestamp"]
                    exchangeTimestamp = eval(result)["data"]["exchangeTimestamp"]
                    # sendTime_resTime = sendTimestampNs - receiveTimestampNs
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]
                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "(exchange, channel, symbol, exchangeTimestamp," \
                          " timestamp, system_time, create_time, gwl ,qel" \
                          "   ) " \
                          "VALUES('1001', 'book',  '{}'," \
                          " '{}','{}' ,'{}', '{}','{}','{}')".format(symbol, exchangeTimestamp, timestamp,
                                                                     system_time, create_time, gwl, qel)

                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))

    @pytest.mark.parametrize('symbol ', li_01)
    def test_02(self, symbol):
        """
        author: Andre
        exchange：1001
        chanel为bbo的情况

        """
        data = {
            "args": {
                "exchange": "1001",
                "symbol": symbol,
                "channel": "bbo"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                if eval(result).get("event") == None:
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]
                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "( exchange, channel, symbol, system_time, create_time" \
                          "  ,gwl,qel) " \
                          "VALUES('1001' , 'bbo',  '{}'," \
                          " '{}', '{}','{}','{}');". \
                        format(symbol, system_time, create_time, gwl, qel)

                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))

    @pytest.mark.parametrize('symbol ', li_01)
    def test_03(self, symbol):
        """
        exchange：1001
        chanel为trades的情况
        author: Andre

        """
        data = {
            "args": {
                "exchange": "1001",
                "symbol": symbol,
                "channel": "trades"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                if eval(result).get("event") == None:
                    # receiveTimestampNs = eval(result).get("data").get("receiveTimestampNs")
                    # sendTimestampNs = eval(result).get("data").get("sendTimestampNs")
                    tradeTime = eval(result).get("data").get("tradeTime")
                    exchangeTimestamp = eval(result)["data"]["exchangeTimestamp"]
                    # sendTime_resTime = sendTimestampNs - receiveTimestampNs
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]

                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "( exchange, channel, symbol, exchangeTimestamp ,system_time, create_time," \
                          "    tradeTime,gwl,qel) " \
                          "VALUES('1001' , 'trades',  '{}', '{}','{}'," \
                          " '{}', '{}', '{}','{}');". \
                        format(symbol, exchangeTimestamp, system_time, create_time, tradeTime, gwl, qel)
                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))

    @pytest.mark.parametrize('symbol', li_02)
    def test_04(self, symbol):
        """
        author: Andre
        exchange：1000
        chanel为book的情况

        """
        data = {
            "args": {
                "exchange": "1000",
                "symbol": symbol,
                "channel": "book"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                if eval(result).get("event") == None:
                    # receiveTimestampNs = eval(result)["data"]["receiveTimestampNs"]
                    # sendTimestampNs = eval(result)["data"]["sendTimestampNs"]
                    timestamp = eval(result)["data"]["timestamp"]
                    exchangeTimestamp = eval(result)["data"]["exchangeTimestamp"]
                    # sendTime_resTime = sendTimestampNs - receiveTimestampNs
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]
                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "(exchange, channel, symbol, exchangeTimestamp," \
                          " timestamp, system_time, create_time, gwl ,qel" \
                          "   ) " \
                          "VALUES('1000', 'book',  '{}'," \
                          " '{}','{}' ,'{}', '{}','{}','{}')".format(symbol, exchangeTimestamp, timestamp,
                                                                     system_time, create_time, gwl, qel)
                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))

    @pytest.mark.parametrize('symbol', li_02)
    def test_05(self, symbol):
        """
        author: Andre
        exchange：1000
        chanel为bbo的情况

        """
        data = {
            "args": {
                "exchange": "1000",
                "symbol": symbol,
                "channel": "bbo"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                logger.info("返回结果是：{}".format(result))
                if eval(result).get("event") == None:
                    exchangeTimestamp = eval(result)["data"]["exchangeTimestamp"]
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]
                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "(exchange, channel, symbol, exchangeTimestamp," \
                          " system_time, create_time, gwl ,qel" \
                          "   ) " \
                          "VALUES('1000', 'bbo',  '{}'," \
                          " '{}','{}' , '{}','{}','{}')".format(symbol, exchangeTimestamp,
                                                                system_time, create_time, gwl, qel)
                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))

    @pytest.mark.parametrize('symbol', li_02)
    def test_06(self, symbol):
        """
        author: Andre
        exchange：1000
        chanel为trades的情况

        """
        data = {
            "args": {
                "exchange": "1000",
                "symbol": symbol,
                "channel": "trades"
            },
            "op": "subscribe"
        }
        ws = create_connection(url=LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(data))
        # 设置的循环次数
        n = 10
        try:
            while n > 0:
                result = ws.recv()
                if eval(result).get("event") == None:
                    exchangeTimestamp = eval(result)["data"]["exchangeTimestamp"]
                    system_time = get_now_time(data="ms")
                    create_time = get_now_time(data="now")
                    gwl = eval(result)["data"]["gwl"]
                    qel = eval(result)["data"]["qel"]
                    sql = "INSERT INTO ltp_lat_monitor.trade_test " \
                          "(exchange, channel, symbol, exchangeTimestamp," \
                          "  system_time, create_time, gwl ,qel" \
                          "   ) " \
                          "VALUES('1000', 'trades',  '{}'," \
                          " '{}','{}' ,'{}', '{}','{}')" \
                        .format(symbol, exchangeTimestamp, system_time, create_time, gwl, qel)
                    db_trade.find_one(sql)
                    n = n - 1
        except Exception as e:
            logger.debug(e)
            logger.debug("{}数据没有找到".format(symbol))


if __name__ == '__main__':
    # pytest.main(['--reruns', '2'])
    pytest.main()
