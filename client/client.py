import socket
import _thread
import os
import threading
In = True
#serverIP = '172.20.2.236'
serverIP = '192.168.43.168'
selfIP = '192.168.43.151'
serverPort = 8080
inf = 1000000
fileList = []
# clientSocket = socket.socket()
# clientSocket.connect((serverIP,serverPort))
# print('连接tracker，请求IPlist！')
# clientSocket.send('JOIN')
# IPlist = clientSocket.recv(1024).split(' ')
# print('获取到IP:')
# print(IPlist)
# mapIdToIps = {}
# for x in range(5000):
#     mapIdToIps[x + 1] = []

def converse(IPlist):
    ids = {}
    for i in range(1000):
        ids[i + 1] = 0
    for ip in IPlist:
        if ip == selfIP:
            continue
        clientSocket = socket.socket()
        print('ip')
        print(ip)
        print('serverIP')
        print(serverIP)
        print(ip == serverIP)
        if ip == serverIP:
            clientSocket.connect((ip,8080))
        else:
            clientSocket.connect((ip,12345))
        clientSocket.send('CHUNK'.encode('utf-8'))
        print('quest chunk list command sent')
        message = ''
        buffer = clientSocket.recv(1024)
        while len(buffer) == 1024:
            message = message + decoding(buffer)
            buffer = clientSocket.recv(1024)
        message = message + decoding(buffer)
        message = message.split(' ')
        for id in message:
            if id == '':
                continue
            tmp_id = int(id)
            ids[tmp_id] = int(ids[tmp_id]) + 1
            mapIdToIps[tmp_id].append(ip)
        clientSocket.close()
        for k in ids:
            if fileList.__contains__(str(k)):
                ids[k] = inf
    for k in ids:
        if ids[k] == 0:
            ids[k] = inf
    ans = sorted(ids,key = ids.__getitem__)
    return ans[0],ans[1],ans[2],ans[3]

# print('解析IPlist')
# ans = converse(IPlist)
# ids = []
# for id in ans:
#     ids.append(int(id[0]))
# ips = [0,0,0,0]
# '''
# 寻找每个id对应的ip
# '''
# for x in range(4):
#     for ip in mapIdToIps[x]:
#         if ips.__contains__(ip) == False:
#             ips[x] = ip
#             break
#     if ips[x] == 0:
#         ips[x] = mapIdToIps[x][0]


def getChunk(ip,id):
    s = socket.socket()
    if ip == serverIP:
        s.connect((ip, 8080))
    else:
        s.connect((ip, 12345))
    s.send(encoding('GET ' + str(id)))
    message = ''
    buffer = s.recv(1024)
    num = 0
    print('begin while')
    while True:
        num = num + 1
        print(str(id) + str(0))
        # print(str(id) + ':' + str(num))
        message = decoding(buffer)
        if message.__contains__('over'):
            file = open('data/' + str(id) + '.txt', 'a')
            file.write(message.replace('over',''))
            file.close()
            break
        file = open('data/' + str(id) + '.txt', 'a')
        file.write(message)
        file.close()
        buffer = s.recv(1024)
        # import time
        # time.sleep(1)
    print(str(id) + ':' + str(num))

    print('end while-----------------------')
    s.close()
    if not fileList.__contains__(str(id)):
        fileList.append(str(id))
    print('end function----------------------------')
    return


# for x in range(4):
#     _thread.start_new_thread(getChunk, (ips[x], ids[x]))


def serve(s):
    command = ''
    command = decoding(s.recv(1024))
    if command.__contains__('CHUNK'):
        ansMessage = ''
        for i in range(len(fileList)):
            if i == 0:
                ansMessage += fileList[i]
            else:
                ansMessage += ' ' + fileList[i]
        print('Ans=' + ansMessage)
        s.send(ansMessage.encode('utf-8'))

    elif command.__contains__('GET'):
        command = command.replace('GET ', '')
        command = command.replace('\r', '')
        command = command.replace('\n', '')
        # 传输chunk
        file = open('./data/' + command + '.txt', 'r')
        num = 0
        while True:
            ansMessage = file.read(1024)
            if ansMessage == '':
                file.close()
                break
            num = num + 1
            print(command + ':' + str(num))
            s.send(ansMessage.encode('utf-8'))
        s.send('over'.encode('utf-8'))

        print(num)
    s.close()


def asServer():
    print('begin')
    serverSocket = socket.socket()
    serverSocket.bind((selfIP, 12345))
    serverSocket.listen(10)
    print('begin to serve!')
    while True:
        s, addr = serverSocket.accept()
        print('connection from:' + addr[0])
        _thread.start_new_thread(serve,(s,))
        if In == False:
            break
    return


def encoding(string):
    return str(string).encode('utf-8')


def decoding(bytess):
    return bytess.decode('utf-8','ignore')


# serverSocket = socket.socket()
# serverSocket.bind((socket.gethostname(),80))
# serverSocket.listen(10)
# s,addr = serverSocket.accept()
# _thread.start_new_thread(serve, (s,))


def checkOver():
    for x in range(100):
        if False == os.path.exists('data/'  + str(x + 1) + '.txt'):
            return False
    return True

for i in range(1,1001):
    if os.path.exists('data/' + str(i) + '.txt'):
        fileList.append(str(i))
#接受请求
import threading
thread = threading.Thread(target = asServer)
thread.start()
import time
time.sleep(1)

clientSocket = socket.socket()
clientSocket.connect((serverIP, serverPort))
print('连接tracker，请求IPlist！')
while True:
    if checkOver():
        clientSocket.send(encoding('QUIT'))
        clientSocket.close()
        print('QUIT')
        exit(1)
        break
    clientSocket.send(encoding('JOIN'))
    print('command sent!')
    tmpMessage = clientSocket.recv(1024)
    IPlist = ''
    while len(tmpMessage) == 1024:
        IPlist = IPlist + decoding(tmpMessage)
        tmpMessage = clientSocket.recv(1024)
    IPlist = IPlist + decoding(tmpMessage)
    IPlist = IPlist.split(' ')
    print('获取到IP:')
    print(IPlist)
    print('test segment!')
    # clientSocket.close()
    mapIdToIps = {}
    for x in range(1000):
        mapIdToIps[x + 1] = []

    print('解析IPlist')
    ans = converse(IPlist)
    print('map')
    print(mapIdToIps)
    print(ans)
    ids = []
    for id in ans:
        ids.append(id)
    ips = [0, 0, 0, 0]
    '''
    寻找每个id对应的ip
    '''
    # print(mapIdToIps)
    for x in range(4):
        for ip in mapIdToIps[ids[x]]:
            if ips.__contains__(ip) == False:
                ips[x] = ip
                break
        if ips[x] == 0 and len(mapIdToIps[ids[x]]) > 0:
            ips[x] = mapIdToIps[ids[x]][0]
    threads = []

    print('ips and ids')
    print(ips)
    print(ids)
    for x in range(4):
        if ips[x] == 0:
            continue
        if fileList.__contains__(ids[x]):
            continue
        thread = threading.Thread(target = getChunk, args = (ips[x], ids[x]))
        thread.start()
        threads.append(thread)
        import time
        time.sleep(1)
    while True:
        print('not over')
        over = True
        for thread in threads:
            print(thread.isAlive())
            if thread.isAlive():
                over = False
        if over == True:
            break
        import time
        time.sleep(1)
