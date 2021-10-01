#!/usr/bin/env python3

import sys
import os
import py
import messages
import pytest
import socket
import ssl
import certifi


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
PSIZE = 2048

context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

'''server_path = py.path.local(__file__).dirpath("server.sh")
server = subprocess.Popen([server_path])


def test_nodb():
    os.system("rm pyserverless.db")
    assert handle_args([""]) == messages.ERROR_NODB


def test_createdb():
    database.initialize_DB()
    database.add_user("tester", "abc123")
    assert database.authenticate_user("tester", "abc123") == True
    assert database.authenticate_user("nonuser", "123abc") == False'''


def test_basic():
    assert sendJsonFile("tests/basic.json") == "10"


def test_function():
    assert sendJsonFile("tests/function.json") == "6"


def test_os_call():
    assert sendJsonFile("tests/advanced.json") == messages.INVALIDCODE


def test_invaliduser():
    assert sendString(
        '{"userName": "teste","authToken": "abc123","Code": "result = 2+2*4"}') == messages.INVALIDAUTH


def test_invalidauth():
    assert sendString(
        '{"userName": "tester","authToken": " ","Code": "result = 2+2*4"}') == messages.INVALIDAUTH


def test_invalidjson():
    assert sendString(
        '<xml>This is not a json</xml>') == messages.INVALIDJSON


def test_invalidCode():
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": " string"}') == messages.INVALIDCODE


def test_disconnect():
    # this should ideally read sever side output
    assert sendDisconnect(
        '{"userName": "teste","authToken": "abc123","Code": "result = 2+2*4"}') == None


def test_longexec():
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": "result=2\\nfor i in range (6,15):\\n\\tresult=result**i\\nresult%=10"}') == "6"


def init_ssl_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            return ssock


def sendString(text):
    ssock = init_ssl_connection()
    ssock.connect((HOST, PORT))
    ssock.sendall(text.encode())
    data = ssock.recv(PSIZE)
    return data.decode()


def sendDisconnect(text):
    ssock = init_ssl_connection()
    ssock.connect((HOST, PORT))
    ssock.sendall(text.encode())
    ssock.close()
    return


def sendJsonFile(filePath):
    ssock = init_ssl_connection()
    ssock.connect((HOST, PORT))
    with open(filePath, "r") as f:
        jText = f.read()
    ssock.sendall(jText.encode())
    data = ssock.recv(PSIZE)
    return data.decode()
