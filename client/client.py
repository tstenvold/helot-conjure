#!/usr/bin/env python3

import socket
import ssl
import certifi

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

context = ssl.create_default_context()


with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print(ssock.version())
        data = ssock.recv(1024)

print('Sent Json Successfully')
print("Received: ", data)
