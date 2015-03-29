#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-24 10:37:11

import threading
import time
import logging
import os

from lib.ping import network_test

logger = logging.getLogger(__name__)


def manage():
    network_status = 0
    while True:
        if network_test('www.baidu.com'):
            logger.info('network is ok')
            if network_status == 0:
                restart_client()  # restart client
                network_status = 1
                time.sleep(60)
        else:
            logger.error('network error')
            network_status == 0
            time.sleep(10)


def restart_client():
    os.system("ps -ef | grep bin/start.py | grep -v grep | awk '{print $2}'  | sed -e 's/^/kill -9 /g' | sh -")
    os.system("cd /data/raspberry-pi-wechat-client && PYTHONPATH=. python bin/start.py &")
    logger.info('restart client ...')


def stop_client():
    os.system('''ps -ef | grep bin/start.py | grep -v grep | awk '{print
        $2}'  | sed -e "s/^/kill -9 /g" | sh -''')
    logger.info('stop client ...')


def deamon():
    t = threading.Thread(target=manage)
    t.start()

if __name__ == '__main__':
    deamon()
