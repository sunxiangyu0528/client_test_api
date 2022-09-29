import json
import time
import _thread as thread
import pytest
import websocket
from _pytest.capture import CaptureManager

from common.log import logger


def manual_step(info):
    capture_manager = CaptureManager("no")
    capture_manager.suspend_global_capture(in_=True)

    while True:
        result = input(info + "  Result:").lower()

        if result in ['fail', 'block', 'j', 'l']:
            comments = input('Comments:')
            if comments:
                break
        elif result in ['pass', 'k']:
            break

    capture_manager.resume_global_capture()

    if result == 'fail' or result == 'j':
        pytest.fail(comments)
    elif result == 'block' or result == 'l':
        pytest.skip(comments)


# 获取当前时间戳方法
def get_now_time(data=None):
    t = time.time()
    if data == "s":
        return int(t)
    elif data == "ms":
        return int(round(t * 1000))
    elif data == "us":
        return int(round(t * 1000000))
    elif data == "now":
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

