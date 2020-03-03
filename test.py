# for x in range(1000,1001):
#     file = open(str(x) + '.txt','w')
#     cnt = 1
#     while  cnt <= 1024 * 256:
#         file.write(str(x))
#         cnt = cnt + len(str(x))
#     file.close()
# file = open('1.txt','r')
# import os
# print(os.path.exists('1.txt'))
# -*- coding: utf-8 -*-

# import socket
#
# '''
# 客户端使用UDP时，首先仍然创建基于UDP的Socket，然后，不需要调用connect()，直接通过sendto()给服务器发数据：
# '''
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# for data in ['a', 'b', 'c']:
#     # 发送数据:
#     s.sendto(data.encode("utf-8"), ('127.0.0.1', 9999))
#     # 接收数据:
#     print(s.recv(1024))
# s.close()

import _thread
import  time
def func(x):
    import time
    time.sleep(1)

import threading
thread = threading.Thread(target = func,args=(1,))
print(thread.isAlive())
thread.start()
print(thread.isAlive())
time.sleep(2)
print(thread.isAlive())