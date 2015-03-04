#! /usr/bin/env python
# coding:utf-8

import socket
import config
import json
import msg_handler
import platform
import logging

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
    login_msg = {'device_id':config.device_id,'info':'login'}
    s.send(json.dumps(login_msg))
    res = json.loads(s.recv(1024))
    status = res['status']
    if status == 0:
        print 'Login Success'
        handleMessage(s)
    elif status == -1:
        print res['err_msg']
        s.close()

def main():
    logging.basicConfig(level=logging.DEBUG)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    system_name = platform.system()
    if system_name == 'Darwin':
        set_keepalive_osx(s)
    elif system_name == 'Linux':
        #利用keepalive保持长连接
        set_keepalive_linux(s)
    s.connect((config.server_host,config.server_port))
    login(s)

def handleMessage(s):
    while True:
        # 持续读取服务器端消息
        recv_msg = s.recv(1024)
        logging.info('receive message %s' % recv_msg)
        req = json.loads(recv_msg)
        key = req.get('key','')
        info = req.get('info','')
        msg_handle = msg_handler.MessageHandler(key, info)
        s.send(msg_handle.handle())

if __name__ == '__main__':
    main()
