import base64
import hmac
import json
import ssl
import threading
import time
from threading import Thread

import websocket
from websocket import WebSocketConnectionClosedException

from common.feishu_robot import FeishuRobot
from config.ws import LTP_URL, OKX_URL, OKX_APIKEY, OKX_PASSPHRASE, OKX_SECRETKEY, BN_PREFIX


class Base:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.flag = True
        self._connect()

    def _connect(self):
        self.ws = websocket.create_connection(url=self.url, sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_message(self, msg):
        pass

    def on_close(self, e):
        pass

    def send_subscribe(self):
        pass

    def on_recv(self):

        def run(x):
            while x.flag:
                try:
                    msg = x.ws.recv()
                    x.on_message(msg)
                except WebSocketConnectionClosedException as e:
                    x.on_close(e)
                    break

        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()


class LTP(Base):

    def __init__(self, url=None, share_dq=None):
        # 判断是否有推送消息过来
        self.is_recv = True
        # 消息缓存
        self.share_dq = share_dq
        # 默认URL
        self.url = url if url else LTP_URL
        super().__init__(self.url)

    def on_recv(self):

        def run(ltp):
            while ltp.flag:
                try:
                    msg = ltp.ws.recv()
                    ltp.on_message(msg)
                except WebSocketConnectionClosedException as e:
                    ltp.on_close(e)
                    break

        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def send_subscribe(self, op="subscribe", channel="book", exchange="1001", symbol="BTC_USDT"):
        subscribe = json.dumps({
            "op": f"{op}",
            "args": {
                "channel": f"{channel}",
                "exchange": f"{exchange}",
                "symbol": f"{symbol}"
            }
        })
        print(f">>>>>>>{subscribe}")
        self.ws.send(subscribe)

    def task_ping(self,op="ping", channel="book", exchange="1001", symbol="BTC_USDT"):
        ping = json.dumps({
            "op": f"{op}",
            "args": {
                "channel": f"{channel}",
                "exchange": f"{exchange}",
                "symbol": f"{symbol}"
            }
        })

        def run(ltp, ping):
            while ltp.flag:
                time.sleep(10)
                try:
                    ltp.ws.send(ping)
                    print(f">>>>>>>{ping}")
                except WebSocketConnectionClosedException as e:
                    print(e)
                    ltp.flag = False

        t = Thread(target=run, args=(self, ping))
        t.daemon = True
        t.start()

    def on_message(self, msg):
        msg = json.loads(msg)
        if msg.get("event") != "pong":
            self.is_recv = True
            if self.share_dq is not None and msg.get("action") == "update":
                self.share_dq.append(msg)
        print(msg)


    def task_check(self):
        def run(ltp):
            count = 0
            while count < 120:
                time.sleep(1)
                if ltp.is_recv:
                    ltp.flag = True
                    ltp.is_recv = False
                    count = 0
                else:
                    count += 1
                    if count == 3:
                        ltp.flag = False
                    print("no data")
            print("============= fail ============")
            msg = json.dumps({"msg": f"【{time.asctime()}】【{threading.current_thread().name}】: ltp no data"})
            a = FeishuRobot.send(msg=msg)

        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def on_close(self, e):
        self.flag = False

    def start(self, ping=True, recv=True, check=False):
        if recv:
            self.on_recv()
        if ping:
            self.task_ping()
        if check:
            self.task_ping()


class OKX(Base):

    def __init__(self, url=None, share_dq=None):
        self.url = url if url else OKX_URL
        self.share_dq = share_dq
        super().__init__(self.url)
        self._login()

    @staticmethod
    def translate(v):
        v = str(v).split("_")
        return "-".join(v)

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

    def _get_sign(self):
        url = "GET/users/self/verify"
        ts = str(time.time())[:14]
        pl = ts + url
        mac = hmac.new(bytes(OKX_SECRETKEY, encoding='utf-8'), bytes(pl, encoding='utf-8'),
                       digestmod='sha256').digest()
        sign = base64.b64encode(mac)
        return ts, sign

    def send_subscribe(self, op="subscribe", channel="books-l2-tbt", instId="ETH_USDT"):
        instId = self.translate(instId)
        subscribe = json.dumps({
            "op": f"{op}",
            "args": [
                {
                    "channel": f"{channel}",
                    "instId": f"{instId}"
                }
            ]
        })
        self.ws.send(subscribe)

    def on_message(self, msg):
        msg = json.loads(msg)
        if msg.get("action") == "update":
            if not self.share_dq is None:
                self.share_dq.append(msg)
        print(msg)

    def start(self, recv=True):
        if recv:
            self.on_recv()


class BN(Base):

    def __init__(self, url=None, symbol="BTC_USDT", share_dq=None):
        self.symbol = self.translate(symbol)
        suffix = f"/ws/{self.symbol}@depth@100ms"
        self.url = url if url else BN_PREFIX + suffix
        self.share_dq = share_dq
        super().__init__(self.url)

    @staticmethod
    def translate(v):
        v = str(v).split("_")
        res = [i.lower() for i in v]
        return "".join(res)

    def on_message(self, msg):
        msg = json.loads(msg)
        if msg.get("e") == "depthUpdate":
            if self.share_dq is not None:
                self.share_dq.append(msg)
        print(msg)


if __name__ == '__main__':
    # bn = BN(symbol="ADA_USDT")
    # bn.on_recv()

    ltp = LTP()
    ltp.send_subscribe(exchange="1000")
    ltp.on_recv()
    ltp.task_ping()

    while True:
        pass
