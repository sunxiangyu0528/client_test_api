import base64
import hmac
import threading
from collections import deque

import requests

from common.feishu_robot import FeishuRobot
from common.log import logger
from config.ws import LTP_URL, OKX_URL, OKX_APIKEY, OKX_PASSPHRASE, OKX_SECRETKEY, BN_PREFIX, FEISHU

import json
import ssl
import time
from threading import Thread

import websocket


class Base:
    subscribe = None

    def __init__(self, url, share_dq=None, debug=True):
        self.share_dq = share_dq
        self.url = url
        self.ws = None
        self.debug = debug
        self._connect()

    def _connect(self):
        self.ws = websocket.create_connection(self.url, sslopt={"cert_reqs": ssl.CERT_NONE})
        print(f"connected {self.url}")

    def send_subscribe(self):
        self.subscribe["op"] = "subscribe"
        self.ws.send(json.dumps(self.subscribe))
        print("==========subscribe==============")

    def on_message(self):
        def run(x):
            while True:
                msg = x.ws.recv()
                if self.debug:
                    logger.debug(msg)
                    print(msg)
                self.msg_handle(msg)
        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def msg_handle(self, msg):
        pass


class LTP(Base):

    subscribe = {
        "op": "subscribe",
        "args": {
            "channel": "book",
            "exchange": "1001",
            "symbol": "BTC_USDT"
        }
    }

    ping = {
        "op": "ping",
        "args": {
            "channel": "book",
            "exchange": "1001",
            "symbol": "BTC_USDT"
        }
    }

    def __init__(self, exchange, symbol, url=None, share_dq=None, debug=True):
        self.url = url if url else LTP_URL
        super().__init__(self.url, share_dq, debug=debug)
        self.catch = None
        self.ping = self._parse_to_json(self.ping, exchange=exchange, symbol=symbol)
        self.subscribe = self._parse_to_json(self.subscribe, exchange=exchange, symbol=symbol)

    @staticmethod
    def _parse_to_json(entry, **kwargs):
        for k, v in kwargs.items():
            entry["args"][k] = v
        return entry

    def task_ping(self):
        def run(ltp):
            while True:
                time.sleep(10)
                ltp.ws.send(json.dumps(ltp.ping))
                if self.debug:
                    print(f"=========={ltp.ping}==============")
        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def task_check(self):
        def run():
            while True:
                # data = {"msg": f"???{time.asctime()}??? {threading.current_thread().name}: ltp no data"}
                time.sleep(30)
                if self.catch:
                    self.catch = None
                    print("check done")
                else:
                    msg = json.dumps({"msg": f"???{time.asctime()}??????{threading.current_thread().name}???: ltp no data"})
                    FeishuRobot.send(msg=msg)
                    print("ltp no data")

        t = Thread(target=run)
        t.daemon = True
        t.start()

    def send_unsubscribe(self):
        self.subscribe["op"] = "unsubscribe"
        print("==========unsubscribe============")
        self.ws.send(json.dumps(self.subscribe))


    def msg_handle(self, msg):
        msg = json.loads(msg)
        if msg.get("event") != "pong":
            self.catch = msg
        if self.share_dq is not None:
            if msg.get("action") == "update":
                ts = time.time()
                msg["get_ts"] = ts
                self.share_dq.append(msg)
        print(msg)

    def start(self):
        self.send_subscribe()
        self.on_message()
        self.task_ping()
        # self.task_check()


class OKX(Base):

    subscribe = {
                    "op": "subscribe",
                    "args": [
                        {
                            "channel": "books-l2-tbt",
                            "instId": "BTC-USDT"
                        }
                    ]
                }

    mp = {
        "BTC_USDT": "BTC-USDT",
        "ETH_USDT": "ETH-USDT"
    }

    def __init__(self, symbol, url=None, share_dq=None, debug=True):
        self.url = url if url else OKX_URL
        if self.mp.get(symbol):
            self.subscribe["args"][0]["instId"] = self.mp.get(symbol)
        else:
            raise Exception("ERROR SYMBOL")
        super().__init__(self.url, share_dq, debug=debug)
        self._login()

    def _login(self):
        ts, sign = self._get_sign()
        data = {
                "op": "login",
                "args": [{"apiKey": OKX_APIKEY,
                          "passphrase": OKX_PASSPHRASE,
                          "timestamp": ts,
                          "sign": sign.decode('utf-8')}]
                }
        self.ws.send(json.dumps(data))
        if self.ws.recv():
            return

    def _hmac_sha256(self, text):
        mac = hmac.new(bytes(OKX_SECRETKEY, encoding='utf-8'), bytes(text, encoding='utf-8'),
                       digestmod='sha256').digest()
        sign = base64.b64encode(mac)
        return sign

    def _get_sign(self):
        url = "GET/users/self/verify"
        ts = str(time.time())[:14]
        pl = ts + url
        return ts, self._hmac_sha256(pl)

    def msg_handle(self, msg):
        if self.share_dq is not None:
            msg = json.loads(msg)
            if msg.get("action") == "update":
                ts = time.time()
                msg["get_ts"] = ts
                self.share_dq.append(msg)

    def start(self):
        self.send_subscribe()
        self.on_message()


class BN(Base):
    mp = {
        "BTC_USDT": "btcusdt",
        "ETH_USDT": "ethusdt"
    }

    def __init__(self, symbol, url=None, share_dq=None, debug=True):
        if not url:
            if self.mp.get(symbol):
                suffix = f"/ws/{self.mp.get(symbol)}@depth@100ms"
            else:
                raise Exception("required symbol")
            self.url = BN_PREFIX + suffix
        else:
            self.url = url

        super().__init__(self.url, share_dq=share_dq, debug=debug)

    def msg_handle(self, msg):
        if self.share_dq is not None:
            msg = json.loads(msg)
            if msg.get("e") == "depthUpdate":
                ts = time.time()
                msg["get_ts"] = ts
                self.share_dq.append(msg)

    def start(self):
        self.on_message()


if __name__ == '__main__':
    data = {"msg": "ltp no data"}
    requests.post(url=FEISHU, json=data)
