#!/usr/bin/env python3

import socket
import pickle
import ssl

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
SIZE = 2048
file = open("client/image_manipulation.py").read()

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.load_default_certs()
sock = socket.socket(socket.AF_INET)
ssock = context.wrap_socket(sock, server_hostname=HOST)
ssock.connect((HOST, PORT))

file = file.replace("\n", "\\n").replace('\"', '\\"')
json = '{ "userName":"tester" ,"authToken":"abc123" ,"Code":"'+file+'"}'
ssock.sendall(json.encode())
data = b''
i=0
while True:
    chunk = ssock.recv(SIZE)
    if len(chunk) < SIZE:
        data += chunk
        break
    data += chunk

result = pickle.loads(data)
result.save("deer_rotated.png")
