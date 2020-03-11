import socket,threading,time,base64,json          #导入socket库
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#创建一个socket对象，AF_INET指定使用IPv4协议(AF_INET6代表IPV6)，SOCK_STREAM指定使用面向流的TCP协议
s.bind(('47.114.165.253',8026))

#监听端口，127.0.0.1是本机地址，客户端必须在本机才能与其连接。端口大于1024的随便找一个
s.listen(5)#开始监听端口，数字表示等待连接的最大数量
print('waiting for connection')

def tcplink(sock,addr):
    print('accept new connection from %s：%s' %addr)              #注意这里addr是一个tuple所以有两个%s
    #从客户端接受消息，最多1024字节
    sock.send(b'ready')
    name = sock.recv(1024).decode('utf-8')
    print('接受用户%s' % name)
    sock.send(b'ready')
    score = int(sock.recv(1024))
    print('成绩为: %d' % score)

    ss = open('serverrecord.json').read()
    record = eval(base64.b64decode(ss[2:-1])) #所有人成绩的字典
    #将用户成绩写入文件
    with open("serverrecord.json", "w") as f:
        if (name in record and record[name] < score) or name not in record:
            record[name] = score
        jsObj = json.dumps(record) # json.dumps()用于将dict类型的数据转成str
        f.write(str(base64.b64encode(str(jsObj).encode('utf-8'))))
        f.close()
    #发送服务端所有成绩
    ss = open('serverrecord.json').read()
    record = str(base64.b64decode(ss[2:-1]))[2:-1] #所有人成绩的字典(str)
    sock.send(record.encode('utf-8')) #向客户端返回服务器的成绩

    sock.close()  #关闭
    print('connection from %s:%s closed' % addr)

while True:               #服务器程序通过一个永久循环来接受来自多个客户端的连接
    sock,addr = s.accept()               #接受一个新连接，用于接收和发送数据。addr是连接的客户端的地址
    t = threading.Thread(target = tcplink,args = (sock,addr))               #创建一个新线程来处理TCP连接（这个很关键）
    t.start()
