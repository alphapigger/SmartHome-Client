# coding:utf-8

import json
import signal
import logging

# from .sensor import ht
from .manage import manager

logger = logging.getLogger(__name__)


class MessageHandler(object):
    def __init__(self, key, info):
        self.key = key
        self.info = info

    def handle(self):
        msg_action = {'LIGHT_ON': self._light_handle,
                      'LIGHT_OFF': self._light_handle,
                      'REAL_TEMPERATURE': self._temperature_handle,
                      }

        return msg_action[self.key]()

    def _light_handle(self):
        if self.key == 'LIGHT_ON':
            command = 'light on'
            info = 'opening'
        elif self.key == 'LIGHT_OFF':
            command = 'light off'
            info = 'closed'
        manager.control(command)
        response = {'status': 0, 'err_msg': '', 'info': info}
        return json.dumps(response)

    def _temperature_handle(self):
        def _timeout_hander(signum, frame):
            raise AssertionError

        try:
            signal.signal(signal.SIGALRM, _timeout_hander)
            signal.alarm(3)
            humidity, temperature = manager.control("humtem")
            signal.alarm(0)
        except AssertionError:
            logger.error('get temperature and humidity timeout...')
            response = {'status': -1,
                        'err_msg': 'ERROR_NODATA',
                        'info': '小兵正在拼死拼活获取数据中，请耐心等待...'}
        else:
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
