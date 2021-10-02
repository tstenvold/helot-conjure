#!/usr/bin/env python3

import socket
import ssl
import certifi

HOST = 'localhost'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.load_default_certs()

sock = socket.socket(socket.AF_INET)
conn = context.wrap_socket(sock, server_hostname=HOST)
conn.connect((HOST, PORT))
conn.sendall(b'{"userName": "tester","authToken": "abc123","Code": "result = 2+2*4"}')
data = conn.recv(1024)
conn.close()

print('Sent Json Successfully')
print("Received: ", repr(data))
