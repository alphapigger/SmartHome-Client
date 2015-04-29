#! /usr/bin/env python
# coding:utf-8

import threading

from client import client
from client.manage.manager import zg_manager


def main():
    t = threading.Thread(target=zg_manager.monitor())
    t1 = threading.Thread(target=zg_manager.hum_tem_work())  # 持续获取湿度温度
    t2 = threading.Thread(target=client.start())
    t2.start()
    t1.start()
    t.start()

if __name__ == '__main__':
    main()
