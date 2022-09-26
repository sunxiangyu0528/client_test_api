import time
import datetime
import _thread as thread
import websocket
import json
import ssl
from common.log import logger
from config.ws import LTP_URL


class TestReConnect(object):

    def test_reconnect(self):
        """
        author: Andre
        websocket因为异常（各种原因）导致连接断开，客户端程序能检查到，自动发起重连
        """

        reconnect_count = 0
        ws = websocket.create_connection(LTP_URL, sslopt={"cert_reqs": ssl.CERT_NONE})
        ping = {
            "op": "ping",
            "args": {
                "channel": "book",
                "exchange": "1001",
                "symbol": "BTC_USDT"
            }
        }

        def on_message(ws, message):

            print("从服务器获取的字符串", message)

        def on_error(ws, error):
            global reconnect_count
            logger.debug("错误类型为：{}".format(type(error)))
            logger.debug("错误：{}".format(error))
            print(type(error))
            print(error)
            if type(error) == ConnectionRefusedError or type(
                    error) == websocket._exceptions.WebSocketConnectionClosedException:
                logger.debug("正在尝试第{}次重连".format(reconnect_count))
                print("正在尝试第{}次重连".format(reconnect_count))
                time.sleep(3)
                logger.debug("重新连接的时间为：{}".format(datetime.datetime.now()))
                print("重新连接的时间为：{}".format(datetime.datetime.now()))
                reconnect_count += 1
                if reconnect_count < 100:
                    connection_tmp(ws)
            else:
                print("其他error!")
                logger.debug("其他error!")

        def on_close(ws):
            print("### closed ###")

        def on_open(ws):
            def run(*args):
                ws.send(json.dumps(ping))
                time.sleep(1)
                ws.close()

            thread.start_new_thread(run, ())

        def connection_tmp(ws):
            websocket.enableTrace(True)
            ws = websocket.WebSocketApp(LTP_URL,
                                        on_message=on_message,
                                        on_error=on_error,
                                        # on_close=on_close
                                        )
            ws.on_open = on_open
            ws.run_forever(ping_interval=10, ping_timeout=5)

        for i in range(5):
            # while True:
            time.sleep(1)
            connection_tmp(ws)
