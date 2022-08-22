import time

import numpy
import pytest

from common.tools import Check
from exchange.ltp import LTP
from exchange.okx import OKX


def test_okx_01():
    """
    author: alex
    logic: 校验极速行情获取的数据和交易所获取的数据的延时
    exception: 延时为
    """
    dq1 = list()
    dq2 = list()
    ltp = LTP(share_dq=dq1)
    okx = OKX(share_dq=dq2)
    okx.start()
    time.sleep(1)
    ltp.start()

    while not dq1:
        print("ltp no data...")
        time.sleep(0.5)

    ltp_data = dq1.pop(0)
    okx_data = dq2.pop(0)
    check = Check(ex_name="OKX")
    while True:
        if check.is_equals(ltp_data, okx_data):
            break
        okx_data = dq2.pop(0)

    count = 0
    ans = []
    while count < 100:
        if dq2 and dq1:
            res = ltp_data['data']["timestamp"] - int(okx_data['data'][0]["ts"])
            # res = (ltp_data["get_ts"] - okx_data["get_ts"]) * 1000
            ans.append(res)
            print(f"========={res}==========")
            print(f"ltp: {ltp_data}")
            print(f"okx: {okx_data}")
            print(f"=========end============")
            okx_data = dq2.pop(0)
            ltp_data = dq1.pop(0)
            count += 1
    assert numpy.median(ans) <= 3


# @pytest.mark.parametrize('n', 100)
def test_okx_02():
    """
    并发在线用户数 n 个
    :return:
    """
    for i in range(5):
        LTP().start()

    while 1:
        pass


def test_okx_03():
    """

    """
