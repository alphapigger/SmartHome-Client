#! /usr/bin/env python
# coding:utf-8

import RPi.GPIO as gpio
import time
import logging
import redis
import random

from .. import settings

logger = logging.getLogger(__name__)


class HTSensor(object):
    def __init__(self, channel=settings['ht_sensor_channel']):
        self.channel = channel
        self.data = []
        self.humidity = None
        self.temperature = None

    def _run(self):
        time.sleep(1)
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.channel, gpio.OUT)
        gpio.output(self.channel, gpio.LOW)
        time.sleep(0.02)
        gpio.output(self.channel, gpio.HIGH)
        gpio.setup(self.channel, gpio.IN)

        while gpio.input(self.channel) == gpio.LOW:
            continue
        while gpio.input(self.channel) == gpio.HIGH:
            continue
        i = 0
        while i < 40:
            k = 0
            while gpio.input(self.channel) == gpio.LOW:
                continue
            while gpio.input(self.channel) == gpio.HIGH:
                k += 1
                if k > 100:
                    break

            if k < 3:
                self.data.append(0)
            else:
                self.data.append(1)
            i += 1
        return self._handle_data()

    def _handle_data(self):
        data = [str(x) for x in self.data]
        humidity = int(''.join(data[0:8]), 2)
        temperature = int(''.join(data[16:24]), 2)
        check = int(''.join(data[32:40]), 2)

        logger.info('humidity: %s temperature: %s check: %s' %
                    (humidity, temperature, check))
        # 湿度+-5误差  温度+-2误差
        if check - 7 <= humidity + temperature <= check + 7:
            self.humidity = humidity
            self.temperature = temperature
            return True
        else:
            return False

    def acquire(self):
        self._run()
        logger.info('%s humidity: %s %% temperature: %s C' %
                    (time.strftime('%H:%M:%S'), self.humidity,
                     self.temperature))
        return self.humidity, self.temperature


def start_monitor():
    ht = HTSensor()
    while True:
        humidity, temperature = ht.acquire()
        i = 0
        while humidity is None or temperature is None:
            time.sleep(2)
            humidity, temperature = ht.acquire()
            if i > 10:
                break
            i += 1
        now = time.strftime('%Y%m%d%H%M')
        r = redis.Redis(host=settings['redis_host'],
                        port=settings['redis_port'],
                        db=settings['redis_db'])
        r.zadd("ht", '%s %s' % (humidity, temperature), int(now))
        time.sleep(600)


def get_data():
    r = redis.Redis(host=settings['redis_host'], port=settings['redis_port'],
                    db=settings['redis_db'])
    now = int(time.strftime('%Y%m%d%H%M'))
    old = now - 10  # 10分钟之前
    h_t = r.zrangebyscore('ht', old, now)
    if h_t:
        humidity, temperature = h_t[-1].split(' ')
        if humidity == 'None' or temperature == 'None':
            ht = HTSensor()
            humidity, temperature = ht.acquire()
            if humidity and temperature:
                r.zadd("ht", '%s %s' % (humidity, temperature), now)
    else:
        humidity, temperature = None, None
    return humidity, temperature

if __name__ == '__main__':
    humidity, temperature = get_data(retry=5)
    if humidity is None and temperature is None:
        print '获取温度失败，请重新获取'
    else:
        print '%s humidity: %s %% temperature: %s C' % \
            (time.strftime('%H:%M:%S'), humidity, temperature)
