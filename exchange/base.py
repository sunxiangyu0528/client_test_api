import json
import ssl
import time
from threading import Thread

import websocket


class BaseExchange:
    subscribe = None

    def __init__(self, url, share_dq=None):
        self.share_dq = share_dq
        self.url = url
        self.ws = self._connect()

    def _connect(self):
        return websocket.create_connection(self.url, sslopt={"cert_reqs": ssl.CERT_NONE})

    def send_subscribe(self):
        def run(x):
            x.ws.send(json.dumps(self.subscribe))
            print("==========subscribe==============")
            while True:
                msg = x.ws.recv()
                print(msg)
                if self.share_dq is not None:
                    msg = json.loads(msg)
                    if msg.get("action") == "update":
                        ts = time.time()
                        msg["get_ts"] = ts
                        self.share_dq.append(msg)

        t = Thread(target=run, args=(self,))
        t.daemon = True
        t.start()



