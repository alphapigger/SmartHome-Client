#! /usr/bin/env python
# coding:utf-8

import threading

import client.client as client
from client.manage.manager import zg_manager


def main():
    t = threading.Thread(target=zg_manager.monitor())
    t1 = threading.Thread(target=zg_manager.hum_tem_work())  # 持续获取湿度温度
    t.start()
    t1.start()
    client.start()

if __name__ == '__main__':
    main()
