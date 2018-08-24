import socket
import sys
from left_pad import left_pad
import time
import struct

META_LEN=4

def assemble_meta(data):
    data_len=len(data.encode())
    meta=struct.pack('!i', data_len)
    return meta

def assemble_payload(data):
    meta=assemble_meta(data)
    return meta+data.encode()

def read_data(client, expect):
    data=client.recv(expect)
    if (len(data)==expect):
        return data
    left=expect-len(data)
    while left>0:
        data+=client.recv(left)
        left=expect-(len(data))
    return data
 
def start_tcp_server(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = (ip, port)
  sock.bind(server_address)
  try:
    sock.listen(1)
  except :
    print("failed to start tcp server")
    sys.exit(1)

  while True:
    print("waiting for connection")
    client, addr = sock.accept()
    print('received a connection')

    try:
        while True:
            meta_data = read_data(client, META_LEN)
            payload_len, = struct.unpack('!i', meta_data)
            payload = read_data(client, payload_len)
            print(str(payload.decode()))       
            ack = assemble_payload('ACK')
            client.send(ack)
    except:
        print(sys.exc_info()[0])
        continue

if __name__ == '__main__':
  server_addr='localhost' 
  server_port=8080
  start_tcp_server(server_addr, server_port)
