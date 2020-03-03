import socket
import _thread
import os
serverIP = '172.20.77.200'
def serve(clientSocket):
    while True:
        command = ''
        buffer = clientSocket.recv(1024)
        while len(buffer) == 0:
            buffer = clientSocket.recv(1024)
            import time
            time.sleep(1)

        while len(buffer) == 1024:
            command = command + buffer.decode('utf-8','ignore')
            buffer = clientSocket.recv(1024)
        command = command + buffer.decode('utf-8','ignore')
        print('command:'+command)

        if command == 'JOIN':
            '发送IP列表'
            sendBuffer = ''
            for x in range(len(IPlist)):
                if not IPlist[x] == addr[0]:
                    sendBuffer = sendBuffer + (IPlist[x]) + ' '
            sendBuffer.strip()
            print(IPlist)
            print("len="+str(len(IPlist)))
            if sendBuffer == '':
                sendBuffer = serverIP
            print(sendBuffer)
            clientSocket.send(sendBuffer.encode('utf-8'))
            '将该客户端加入IPlist'
            if not IPlist.__contains__(addr[0]):
                IPlist.append(addr[0])
            print(addr[0] + ' has joined the group!')
            print('tmp list:')
            print(IPlist)

        elif command == 'QUIT':
            IPlist.remove(addr[0])
            print(addr[0] + ' has been removed from tracker!')
            break

        elif command.__contains__('CHUNK'):
            ansMessage = ''
            for i in range(1,101):
                if os.path.exists('./data/' + str(i) + '.txt'):
                    ansMessage += str(i)
                if i != 100:
                    ansMessage += ' '
            print('Ans=' + ansMessage)
            clientSocket.send(ansMessage.encode('utf-8'))

        elif command.__contains__('GET'):
            command = command.replace('GET ','')
            command = command.replace('\r','')
            command = command.replace('\n','')
            #传输chunk
            file = open('./data/' + command + '.txt','r')
            num = 0
            while True:
                ansMessage = file.read(1024)
                if ansMessage == '':
                    file.close()
                    break
                num = num + 1
                print(command + ':' + str(num))
                clientSocket.send(ansMessage.encode('utf-8'))
            clientSocket.send('over'.encode('utf-8'))

            print(num)

        elif not command == '':
            print(command)
            print('bad request!')
        
    clientSocket.close()

IPlist = []
serverPort = 8080
serverSocket = socket.socket()
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(10)
print('tracker start work!')
print('tracker message:')
print('hostname' + socket.gethostname())
print('port' + str(serverPort))


#主循环
while True:
    print("QAQ")
    clientSocket, addr = serverSocket.accept()
    print('accept connection from:')
    print(addr)
    _thread.start_new_thread(serve, (clientSocket,))