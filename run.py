import pytest
import schedule


def job1():
    pytest.main(["./cases/trade/test_reconnect.py", "-v", "-s"])


def job2():
    pytest.main(["./cases/trade/test_insert_sql.py", "-v", "-s", "--reruns", "3"])


def job3():
    pytest.main(["./cases/trade/test_fast_market.py"])
    pytest.main(["./cases/trade/test_fast_market1.py"])


schedule.every(1).day.do(job1)  # 每隔 1天运行一次 job 函数
schedule.every(10).minutes.do(job2)  # 每隔 10 分钟运行一次 job 函数
schedule.every(10).minutes.do(job3)  # 每隔 10 分钟运行一次 job 函数

while True:
    schedule.run_pending()
