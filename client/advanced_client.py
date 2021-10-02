#!/usr/bin/env python3

import socket
import pickle
from PIL import Image
import io

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
SIZE = 2048
file = open("client/image_manipulation.py").read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    file = file.replace("\n", "\\n").replace('\"', '\\"')
    json = '{ "userName":"tester" ,"authToken":"abc123" ,"Code":"'+file+'"}'
    s.sendall(json.encode())
    data = b''
    i=0
    while True:
        chunk = s.recv(SIZE)
        if len(chunk) < SIZE:
            data += chunk
            break
        data += chunk

result = pickle.loads(data)
result.save("deer_rotated.png")
