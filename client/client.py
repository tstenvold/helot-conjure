#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{ "authToken":"abc123", "Code":"1+5*6"}')
    data = s.recv(1024)

print('Sent Json Successfully')
print('Received', repr(data))
