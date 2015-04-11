#! /usr/bin/env python
# coding:utf-8

import serial


class BaseManage(object):
    '''
    '''
    def __init__(self):
        pass


def main():
    com = serial.Serial("/dev/ttyAMA0", 38400, bytesize=8, parit='N',
                        stopbits=1, timeout=0, xonxoff=0, rtscts=0)
    while True:
        command = raw_input("Enter command")
        com.write(command)

if __name__ == '__main__':
    main()
