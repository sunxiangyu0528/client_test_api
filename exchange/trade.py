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
        self._connect()

    def _connect(self):
        self.ws = websocket.create_connection(url=self.url, sslopt={"cert_reqs": ssl.CERT_NONE})

    def send_subscribe(self):
        pass

    def on_recv(self):

        def run(x):
            while True:
                try:
                    msg = x.ws.recv()
                    x.on_message(msg)
                except WebSocketConnectionClosedException as e:
                    x.on_close(e)
                    break

        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def on_message(self, msg):
        print(msg)

    def on_colse(self, e):
        pass


class LTP(Base):

    def __init__(self, url=None):
        self.is_recv = True
        self.flag = True
        self.url = url if url else LTP_URL
        super().__init__(self.url)

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

    def task_ping(self):
        ping = json.dumps({"op": "ping"})

        def run(ltp, ping):
            while True:
                time.sleep(10)
                try:
                    ltp.send(ping)
                except WebSocketConnectionClosedException as e:
                    print(e)
                    ltp.flag = False
                    break

        t = Thread(target=run, args=(self, ping))
        t.daemon = True
        t.start()

    def on_message(self, msg):
        msg = json.loads(msg)
        if msg.get("action") == "update":
            self.is_recv = True
        # print(msg)

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

        t = Thread(target=run, args=(self, ))
        t.daemon = True
        t.start()

    def on_colse(self, e):
        self.flag=False


class OKX(Base):
    mp = {
        "BTC_USDT": "BTC-USDT",
        "ETH_USDT": "ETH-USDT"
    }

    def __init__(self, url=None):
        self.url = url if url else OKX_URL
        super().__init__(self.url)
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

    def _get_sign(self):
        url = "GET/users/self/verify"
        ts = str(time.time())[:14]
        pl = ts + url
        mac = hmac.new(bytes(OKX_SECRETKEY, encoding='utf-8'), bytes(pl, encoding='utf-8'),
                       digestmod='sha256').digest()
        sign = base64.b64encode(mac)
        return ts, sign

    def send_subscribe(self, op="subscribe", channel="books-l2-tbt", instId="BTC_USDT"):
        subscribe = json.dumps({
            "op": f"{op}",
            "args": [
                {
                    "channel": f"{channel}",
                    "instId": f"{self.mp.get(instId)}"
                }
            ]
        })
        self.ws.send(subscribe)


class BN(Base):
    mp = {
        "BTC_USDT": "btcusdt",
        "ETH_USDT": "ethusdt"
    }

    def __init__(self, url=None, symbol="BTC_USDT"):
        suffix = f"/ws/{self.mp.get(symbol)}@depth@100ms"
        self.url = url if url else BN_PREFIX + suffix
        super().__init__(self.url)


if __name__ == '__main__':
    # a = time.time()
    # ltp = LTP()
    # ltp.send_subscribe()
    # ltp.on_recv()
    # ltp.task_check()
    # time.sleep(30)
    # ltp.send_subscribe(op="unsubscribe")
    # while ltp.flag:
    #     pass
    # b = time.time()
    # print(a-b)
    okx = OKX()
    okx.on_recv()
    okx.send_subscribe(op="oooo")
    time.sleep(1)
    # okx.send_subscribe()



    while 1:
        pass
