#! /usr/bin/env python
# coding:utf-8
import socket
import json
import platform
import logging

from . import settings
from . import msg_handler

logger = logging.getLogger(__name__)


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.
    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


def set_keepalive_osx(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.
    sends a keepalive ping once every 3 seconds (interval_sec)
    """
    # scraped from /usr/include, not exported by python's socket module
    TCP_KEEPALIVE = 0x10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, interval_sec)


def login(s):
    login_msg = {'device_id': settings['device_id'], 'info': 'login'}
    s.send(json.dumps(login_msg))
    res = json.loads(s.recv(1024))
    status = res['status']
    if status == 0:
        logger.info('Login Success')
        handleMessage(s)
    elif status == -1:
        print res['err_msg']
        s.close()


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    system_name = platform.system()
    if system_name == 'Darwin':
        set_keepalive_osx(s)
    elif system_name == 'Linux':
        set_keepalive_linux(s)
    s.connect((settings['server_host'], settings['server_port']))
    login(s)


def handleMessage(s):
    while True:
        recv_msg = s.recv(1024)
        logger.info('receive message %s' % recv_msg)
        msg_handle = msg_handler.MessageHandler(json.loads(recv_msg))
        s.send(msg_handle.handle())

if __name__ == '__main__':
    start()
