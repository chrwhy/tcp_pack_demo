from socket import *
from left_pad import left_pad
import time

def assemble_meta(data):
    data_len=len(data.encode())
    meta=str(left_pad(str(data_len), META_LEN-len(str(data_len)), '0'))
    return meta

def assemble_payload(data):
    meta=assemble_meta(data)
    return meta.encode()+data.encode() 

def read_data(conn, expect):
    data=conn.recv(expect)
    if data is None:
        return None
    if (len(data)==expect):
        return data
    left=expect-len(data)
    while left>0:
        data+=client.recv(left)
        left=expect-(len(data))
    return data

META_LEN=4
serverName = 'localhost'
serverPort = 8080
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

hello='Hello Server'
payload=assemble_payload(hello)
clientSocket.send(payload)

time.sleep(1)
        
while (True):
    f = open('auto_test.txt','r', encoding='utf-8') 
    for line in f.readlines():        
        print(line)

        payload=assemble_payload(line)
        clientSocket.send(payload)

        meta_data = read_data(clientSocket, META_LEN)
        if meta_data is None:
           continue

        payload_len = int(meta_data.decode())
        payload = read_data(clientSocket, payload_len)
        print('From server: ' + payload.decode())
        time.sleep(2)
clientSocket.close()

