import base64
import hmac
import json
import time

from exchange.base import BaseExchange
from config.ws import OKX_APIKEY, OKX_PASSPHRASE, OKX_SECRETKEY, OKX_URL


class OKX(BaseExchange):

    subscribe = {
                    "op": "subscribe",
                    "args": [
                        {
                            "channel": "books-l2-tbt",
                            "instId": "BTC-USDT"
                        }
                    ]
                }

    def __init__(self, url=None, share_dq=None, **kwargs):
        self.url = url if url else OKX_URL
        super().__init__(self.url, share_dq)
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

    def start(self):
        self.send_subscribe()


if __name__ == '__main__':
    a = OKX()
    a.start()



