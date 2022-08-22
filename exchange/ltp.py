import json
import time
from threading import Thread

from exchange.base import BaseExchange
from config.ws import LTP_URL


class LTP(BaseExchange):

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

    def __init__(self, url=None, share_dq=None, **kwargs):
        self.url = url if url else LTP_URL
        super().__init__(self.url, share_dq)
        self.ping = self._parse_to_json(self.ping, **kwargs)
        self.subscribe = self._parse_to_json(self.subscribe, **kwargs)

    @staticmethod
    def _parse_to_json(entry, **kwargs):
        for k, v in kwargs.items():
            entry["args"][k] = v
        return entry

    def task_ping(self):
        def run(ltp):
            while True:
                ltp.ws.send(json.dumps(ltp.ping))
                print("==========ping==============")
                time.sleep(10)
        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()

    def start(self):
        self.send_subscribe()
        self.task_ping()


if __name__ == '__main__':
    ltp = LTP()
    ltp.start()