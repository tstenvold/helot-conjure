#!/usr/bin/env python3

import socket
import pytest
from messages import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
PSIZE = 2048


def test_basic():
    assert sendJsonFile("tests/basic.json") == "10"


def test_function():
    assert sendJsonFile("tests/function.json") == "6"


def test_invaliduser():
    assert sendString(
        '{"userName": "teste","authToken": "abc123","Code": "result = 2+2*4"}') == INVALIDAUTH


def test_invalidauth():
    assert sendString(
        '{"userName": "tester","authToken": " ","Code": "result = 2+2*4"}') == INVALIDAUTH


def test_invalidjson():
    assert sendString(
        '<xml>This is not a json</xml>') == INVALIDJSON


def test_invalidCode():
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": " string"}') == INVALIDCODE


def test_longexec():
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": "result=2\\nfor i in range (6,15):\\n\\tresult=result**i\\nresult%=10"}') == "6"


def sendString(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        con.sendall(text.encode())
        data = con.recv(PSIZE)
        return data.decode()


def sendJsonFile(filePath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        with open(filePath, "r") as f:
            jText = f.read()

        con.sendall(jText.encode())
        data = con.recv(PSIZE)
        return data.decode()
