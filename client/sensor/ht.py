#! /usr/bin/env python
# coding:utf-8

import RPi.GPIO as gpio
import time
import logging

from .. import settings

logger = logging.getLogger(__name__)


class HTSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.data = []
        self.humidity = None
        self.temperature = None

    def _run(self):
        time.sleep(0.5)
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
        if humidity + temperature == check:
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


def get_data(retry):
    channel = settings['ht_sensor_channel']
    ht = HTSensor(channel)

    for i in xrange(retry):
        humidity, temperature = ht.acquire()
        if humidity is not None and temperature is not None:
            break

    return humidity, temperature

if __name__ == '__main__':
    humidity, temperature = get_data(retry=5)
    if humidity is None and temperature is None:
        print '获取温度失败，请重新获取'
    else:
        print '%s humidity: %s %% temperature: %s C' % \
            (time.strftime('%H:%M:%S'), humidity, temperature)
