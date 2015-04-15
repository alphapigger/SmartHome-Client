#! /usr/bin/env python
# coding:utf-8

import threading

import client.client as client
from client.manage import manager


def main():
    t = threading.Thread(target=manager.start_monitor)
    t.start()
    client.start()

if __name__ == '__main__':
    main()
