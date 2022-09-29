import time
import datetime
import _thread as thread
import websocket
import json
import ssl
from common.log import logger
from config.ws import LTP_URL
import _thread


class TestReConnect(object):

    def test_reconnect(self):
        """
        author: Andre
        websocket因为异常（各种原因）导致连接断开，客户端程序能检查到，自动发起重连
        """

        reconnect_count = 0

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
                on_open(ws)
                logger.debug("重新连接的时间为：{}".format(datetime.datetime.now()))
                print("重新连接的时间为：{}".format(datetime.datetime.now()))
                reconnect_count += 1
                if reconnect_count < 100:
                    print("reconnect_count小于100")

            else:
                print("其他error!")
                logger.debug("其他error!")

        def on_open(ws):
            # 线程运行函数
            def process():
                ping = {
                    "args": {
                        "exchange": "1001",
                        "symbol": "XRP_USDT",
                        "channel": "trades"
                    },
                    "op": "ping"
                }
                subscribe = {
                    "args": {
                        "exchange": "1001",
                        "symbol": "XRP_USDT",
                        "channel": "trades"
                    },
                    "op": "subscribe"
                }

                ws.send(json.dumps(subscribe))
                # 休息 0.2 秒先接收服务器回复的消息
                time.sleep(0.2)
                while True:
                    time.sleep(10)
                    ws.send(json.dumps(ping))
                # 关闭 Websocket 的连接

                ws.close()
                print("Websocket closed")

            thread.start_new_thread(process, ())

        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(LTP_URL,
                                    on_message=on_message,
                                    on_error=on_error,
                                    )
        ws.on_open = on_open
        ws.run_forever()
