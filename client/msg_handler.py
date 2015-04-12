# coding:utf-8

import time
import json
# import signal
import logging

# from .sensor import ht
from .manage import manager

logger = logging.getLogger(__name__)


class MessageHandler(object):
    def __init__(self, key, info):
        self.key = key
        self.info = info

    def handle(self):
        msg_action = {'LIGHT_ON': self.lightHandle,
                      'LIGHT_OFF': self.lightHandle,
                      'REAL_TEMPERATURE': self.temperatureHandle,
                      }

        return msg_action[self.key]()

    def lightHandle(self):
        response = {'status': 0, 'err_msg': '', 'info': self.key}
        time.sleep(1)
        return json.dumps(response)

    def temperatureHandle(self):
        # def _timeout_handler(signum, frame):
        #     raise AssertionError
        # try:
        #     signal.signal(signal.SIGALRM, _timeout_handler)
        #     signal.alarm(2)  # 超时时间为2秒
        #     humidity, temperature = ht.get_data()
        #     signal.alarm(0)
        #     response = {'status': 0,
        #                 'err_msg': '',
        #                 'info': {'humidity': humidity,
        #                          'temperature': temperature},
        #                 }
        #     return json.dumps(response)
        # except AssertionError:
        #     logger.info('Acquire humidity and temperature timeout')
        #     response = {'status': -1,
        #                 'err_msg': '请检查温度湿度传感器的连接',
        #                 'info': '温度湿度传感器或许未连接'}
        #     return json.dumps(response)

        # humidity, temperature = ht.get_data()
        manager.control("light on")
        humidity, temperature = None, None
        if humidity is None or temperature is None:
            response = {'status': -1,
                        'err_msg': 'ERROR_NODATA',
                        'info': '小兵正在拼死拼活获取数据中，请耐心等待...'}
        else:
            response = {'status': 0,
                        'err_msg': '',
                        'info': {'humidity': humidity,
                                 'temperature': temperature},
                        }
        return json.dumps(response)
