#!/usr/bin/env python3

import socket
import database
from serverjson import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
ex_locals = {}


def startServer():
    while True:  # infinite loop waiting for connections

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(2048)
                    if not data:
                        break

                    jsonObj = textToJson(data)
                    jCode = jsonCode(jsonObj)
                    uName = jsonUserName(jsonObj)
                    aCode = jsonAuthToken(jsonObj)

                    # TODO
                    # validate JSON
                    # kick off into own thread and time
                    if(database.authenticate(uName, aCode)):
                        print("\n Code:")
                        print(jCode)
                        exec(jCode, None, ex_locals)
                        result = str(ex_locals['result'])
                        conn.sendall(result.encode())
                    else:
                        print("Invalid User/Auth")
                        conn.sendall(str("Invalid User/Auth").encode())
