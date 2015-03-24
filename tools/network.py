#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-24 10:37:11

import threading
import time

from lib.ping import network_test


def manage():
    network_status = 0
    while True:
        if network_test('www.baidu.com'):
            print 'Network Ok'
            if network_status == 0:
                print 'Restart Program'
                network_status = 1
        else:
            print 'Network error'
            network_status == 0
        time.sleep(10)

def main():
    t = threading.Thread(target=manage)
    t.start()

if __name__ == '__main__':
    main()
