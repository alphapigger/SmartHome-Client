#! /usr/bin/env python
# coding:utf-8

import serial
import logging
import json

from ..lib import mcurl
from .. import settings

logger = logging.getLogger(__name__)


class ClinetManager(object):
    '''
    '''
    port = "/dev/ttyAMA0"
    rate = 38400

    CMD_REGISTER = 1   # 数据格式为 1 device_id device_type
    CMD_HUMTEM = 2     # 数据格式  2 device_id hum tem

    SENSORS = list()

    def __init__(self):
        self.com = serial.Serial(self.port, self.rate)

    def read(self):
        data = self.com.readline()
        logger.info('Receive msg : %r', data)
        return data

    def write(self, msg):
        msg += "\\"
        length = self.com.write(msg)
        logger.info("Send msg: %r, length is: %s", msg, length)


manager = ClinetManager()
curl = mcurl.CurlHelper()


def control(sensor_id, value):
    command = "%s %s" % (sensor_id, value)
    manager.write(command)


def register_sensors(self, device_id, sensor_id, sensor_type):
    api_url = settings['device_info_api']
    post_data = {'device_id': device_id, 'sensor_id': sensor_id,
                 'sensor_type': sensor_type}
    logger.info('device_id %r register sensor_id %s sensor_type %s',
                device_id, sensor_id, sensor_type)
    res = curl.post(api_url, data=json.dumps(post_data))
    logger.info('Receive msg from server: %r', res)


def upload_sensor_data(self, device_id, sensor_id, sensor_value):
    api_url = settings['sensor_data_api']
    post_data = {'device_id': device_id, 'sensor_id': sensor_id,
                 'value': sensor_value}
    logger.info('upload device_id %s sensor_id %s value: %s',
                device_id, sensor_id, sensor_value)
    res = curl.post(api_url, data=json.dumps(post_data))
    logger.info('Receive msg from server: %s', res)


def start_monitor():
    while True:
        data = manager.read()
        data = data.split()
        command = data[0]
        if command == manager.CMD_REGISTER:
            sensor_id = data[1]
            sensor_type = data[2]  # 1 hum&tem  2 led
            device_id = settings['device_id']
            manager.SENSORS.append({"id": sensor_id, "type": sensor_type})
            register_sensors(device_id, sensor_id, sensor_type)
        elif command == manager.CMD_HUMTEM:
            sensor_id = data[1]
            humidity = data[2]
            temperature = data[3]

            upload_sensor_data(settings['device_id'],
                               sensor_id, '%s,%s' % (humidity, temperature))


def main():
    manager.read()
    manager.write("light on")

if __name__ == '__main__':
    main()
