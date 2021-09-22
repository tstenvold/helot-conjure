#!/usr/bin/env python3

import socket
import pytest
from messages import *

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server


class TestJsonFiles:

    def test_basic(self):
        assert sendJsonFile("tests/basic.json") == "10"

    def test_function(self):
        assert sendJsonFile("tests/function.json") == "6"

    def test_invaliduser(self):
        assert sendString(
            '{"userName": "teste","authToken": "abc123","Code": "result = 2+2*4"}') == INVALIDAUTH

    def test_invalidauth(self):
        assert sendString(
            '{"userName": "tester","authToken": " ","Code": "result = 2+2*4"}') == INVALIDAUTH

    def test_invalidCode(self):
        assert sendString(
            '{"userName": "tester","authToken": "abc123","Code": " string"}') == INVALIDCODE


def sendString(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        con.sendall(text.encode())
        data = con.recv(2048)
        return data.decode()


def sendJsonFile(filePath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        with open(filePath, "r") as f:
            jText = f.read()

        con.sendall(jText.encode())
        data = con.recv(2048)
        return data.decode()
