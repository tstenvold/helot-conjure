#!/usr/bin/env python3

import socket
import pytest

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server


class TestJsonFiles:

    def test_basic(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            assert sendJsonFile(s, "tests/basic.json") == "10"
            s.close()

    def test_function(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            assert sendJsonFile(s, "tests/function.json") == "6"
            s.close()


def sendJsonFile(con, filePath):
    f = open(filePath, "r")
    jText = f.read()
    f.close()
    con.sendall(jText.encode())
    data = con.recv(2048)
    return data.decode()
