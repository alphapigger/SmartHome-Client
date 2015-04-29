#! /usr/bin/env python
# coding:utf-8

import threading

import client.client as client
from client.manage.manager import zg_manager


def main():
    t = threading.Thread(target=zg_manager.monitor())
    t.start()
    client.start()

if __name__ == '__main__':
    main()
