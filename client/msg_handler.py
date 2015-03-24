# coding:utf-8

import time
import json

class MessageHandler(object):
    def __init__(self,key,info):
        self.key = key
        self.info = info

    def handle(self):
        msg_action = {
        'LIGHT_ON':self.lightHandle,
        'LIGHT_OFF': self.lightHandle,
        'REAL_TEMPERATURE': self.temperatureHandle,
        }

        return msg_action[self.key]()

    def lightHandle(self):
        response = {'status':0,'err_msg':'','info':self.key}
        time.sleep(1)
        return json.dumps(response)

    def temperatureHandle(self):
        response = {'status':0,'err_msg':'','info':self.key}
        time.sleep(1)
        return json.dumps(response)
