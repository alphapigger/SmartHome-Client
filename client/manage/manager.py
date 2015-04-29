#! /usr/bin/env python
# coding:utf-8

import serial
import logging
import json
import redis
import time

try:
    import cPickle as pickle
except:
    import pickle

from ..lib import mcurl
from .. import settings

logger = logging.getLogger(__name__)
curl = mcurl.CurlHelper()
rconn = redis.Redis(
    host=settings['redis_host'],
    port=settings['redis_port'],
    db=settings['redis_db'],
)


class Sensor(object):
    HUM_TEM_TYPE = 3
    LED_TYPE = 4

    def __init__(self, device_id, sensor_id, sensor_type, sensor_value=None):
        self._retrieve_sensors()
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value
        self.sensors.update({str(sensor_id): {'type': int(sensor_type)}})
        self._persist_sensors()

    def _retrieve_sensors(self):
        if not rconn.exists('sensors'):
            rconn.set("sensors", pickle.dumps(dict()))
        self.sensors = pickle.loads(rconn.get('sensors'))

    def _persist_sensors(self):
        rconn.set("sensors", pickle.dumps(self.sensors))


class SensorManager(object):
    '''SensorManager
    '''

    @classmethod
    def register(cls, sensor):
        register_url = settings['sensor_register_api'] % sensor.device_id
        data = {
            'device_id': sensor.device_id,
            'sensor_id': sensor.sensor_id,
            'sensor_type': sensor.sensor_type
        }
        logger.info('api: %s, data: %r', register_url, data)
        res = curl.post(
            register_url, data=json.dumps(data),
        )
        logger.info('Register sensor: %r, response: %r', data, res)

    @classmethod
    def upload(cls, sensor):
        upload_url = settings['sensor_data_api'] % (sensor.device_id, sensor.sensor_id)
        data = {
            'device_id': sensor.device_id,
            'sensor_id': sensor.sensor_id,
            'value': sensor.sensor_value
        }
        logger.info('api: %s, data: %r', upload_url, data)
        res = curl.post(upload_url, data=json.dumps(data))
        logger.info('Upload sensor data: %r, response: %r', data, res)


class ZigManager(object):
    '''ZigManager
    '''
    SERIAL_PORT = '/dev/ttyAMA0'
    SERIAL_RATE = 38400

    CMD_REGISTER = 1
    CMD_DATA = 2

    def __init__(self):
        self.com = serial.Serial(self.SERIAL_PORT, self.SERIAL_RATE)

    def read(self):
        data = self.com.readline()
        logger.info('Read msg: %r', data)
        return data

    def write(self, msg):
        msg += "\\"
        length = self.com.write(msg)
        logger.info('Write msg: %r, len is: %s', msg, length)

    def monitor(self):
        while True:
            data = self.read().split()
            device_id = settings['device_id']
            cmd = data[0]
            sensor_id = data[1]
            sensor_type = data[2]
            if cmd == self.CMD_REGISTER:
                sensor = Sensor(device_id, sensor_id, sensor_type)
                SensorManager.register(sensor)
            elif cmd == self.CMD_DATA:
                sensor_value = data[3]
                sensor = Sensor(device_id, sensor_id, sensor_type, sensor_value)
                SensorManager.upload(sensor)

    def hum_tem_work(self):
        while True:
            time.sleep(120)
            sensors = pickle.loads(rconn.get('sensors'))
            for id, info in sensors.items():
                if info['type'] == Sensor.HUM_TEM_TYPE:
                    cmd = "%s" % id
                    self.write(cmd)

zg_manager = ZigManager()
