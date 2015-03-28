#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-24 10:37:11

import threading
import time
import logging
import yaml
import logging.config

settings = yaml.load(open('settings.yml'))
logging.config.dictConfig(settings['logging'])

from lib.ping import network_test

logger = logging.getLogger(__name__)


def manage():
    network_status = 0
    while True:
        if network_test('www.baidu.com'):
            logger.info('network is ok')
            if network_status == 0:
                network_status = 1
                time.sleep(60)
        else:
            logger.error('network error')
            network_status == 0
            time.sleep(10)


def main():
    t = threading.Thread(target=manage)
    t.start()

if __name__ == '__main__':
    main()
