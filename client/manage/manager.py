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

    def __init__(self):
        self.com = serial.Serial(self.port, self.rate)

    def read(self):
        data = self.com.readline()
        logger.info('Receive msg : %r', data)

    def receive(self):
        while True:
            self.read()

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


def start_monitor():
    manager.receive()


def main():
    manager.read()
    manager.write("light on")

if __name__ == '__main__':
    main()
