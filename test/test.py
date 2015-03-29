#! /usr/bin/env python
# coding:utf-8
import socket
import json


def login(s):
    login_msg = {'device_id': 1, 'info': 'login'}
    s.send(json.dumps(login_msg))
    res = json.loads(s.recv(1024))
    print res
    status = res['status']
    if status == 0:
        print 'Login Success'
    elif status == -1:
        print res['err_msg']
        s.close()


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('54.148.6.4', 8888))
    login(s)


def handleMessage(s):
    while True:
        # 持续读取服务器端消息
        recv_msg = s.recv(1024)
        req = json.loads(recv_msg)
        key = req.get('key', '')
        info = req.get('info', '')
        msg_handle = msg_handler.MessageHandler(key, info)
        s.send(msg_handle.handle())

if __name__ == '__main__':
    start()
