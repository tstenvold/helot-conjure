#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(
        b'{ "userName":"teste" ,"authToken":"abc123", "Code":"result = 2 \\nfor i in range (5,9): \\n\\tresult = result**i "}')
    data = s.recv(2048)


print('Sent Json Successfully')
print('Received', repr(data))
