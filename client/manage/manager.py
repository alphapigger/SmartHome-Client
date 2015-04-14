#! /usr/bin/env python
# coding:utf-8

import serial
import logging

logger = logging.getLogger(__name__)


class ClinetManager(object):
    '''
    '''
    port = "/dev/ttyAMA0"
    rate = 38400

    CMD_REGISTER = 1   # 数据格式为 1 device_id device_type
    CMD_HUMTEM = 2     # 数据格式  2 device_id hum tem
    CMD_LED = 3        # 数据格式 3 device_id 0/1

    def __init__(self):
        self.com = serial.Serial(self.port, self.rate)

    def read(self):
        data = self.com.readline()
        logger.info('Receive msg : %r', data)
        return data

    def write(self, msg):
        msg += "\\"
        length = self.com.write(msg)
        logger.info("Send msg: %r, length is: %s", msg, length)


manager = ClinetManager()


def control(msg):
    if msg == "light on":
        manager.write("light on")
    elif msg == "light off":
        manager.write("light off")
    elif msg == "humtem":
        manager.write("humtem")
        resp = manager.read()
        resp = resp.split(' ')
        if len(resp) == 3:
            return resp[1], resp[2]
        else:
            return None, None


def start_monitor():
    while True:
        data = manager.read()
        data = data.split()
        command = data[0]
        if command == manager.CMD_REGISTER:
            device_id = data[1]
            device_type = data[2]
        elif command == manager.CMD_HUMTEM:
            device_id = data[1]
            hum = data[2]
            tem = data[3]



def main():
    manager.read()
    manager.write("light on")

if __name__ == '__main__':
    main()
