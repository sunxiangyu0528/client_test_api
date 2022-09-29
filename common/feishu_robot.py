import json
import threading
import time

import requests

# from client_test_api.config.ws import FEISHU
from config.ws import FEISHU

class FeishuRobot:
    webhook = FEISHU
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    @classmethod
    def send(cls, msg):
        return requests.post(url=cls.webhook, data=msg, headers=cls.headers)


if __name__ == '__main__':
    msg = json.dumps({"msg": f"【{time.asctime()}】【{threading.current_thread().name}】: ltp no data"})
    a = FeishuRobot.send(msg=msg)
    print("df")
