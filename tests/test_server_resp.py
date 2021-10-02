#!/usr/bin/env python3

import sys
import os
import py
import messages
import pytest
import socket
import pickle
from PIL import Image
import urllib.request
from io import BytesIO


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
SIZE = 2048

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
    assert sendJsonFile("tests/basic.json") == 10


def test_function():
    assert sendJsonFile("tests/function.json") == 6


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
        '{"userName": "tester","authToken": "abc123","Code": "result=2\\nfor i in range (6,15):\\n\\tresult=result**i\\nresult%=10"}') == 6

def test_image_rotate():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        file = open("client/image_manipulation.py").read()

        urllib.request.urlretrieve("https://opensource.com/sites/default/files/images/jupyter-image_7_0.png", "deer.jpg")
        img = Image.open("deer.jpg")
        result = img.rotate(90)

        file = file.replace("\n", "\\n").replace('\"', '\\"')
        json = '{ "userName":"tester" ,"authToken":"abc123" ,"Code":"'+file+'"}'
        con.sendall(json.encode())

        data = b''
        i=0
        while True:
            chunk = con.recv(SIZE)
            if len(chunk) < SIZE:
                data += chunk
                break
            data += chunk
        os.remove("deer.jpg")
        assert result == pickle.loads(data)


def sendString(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        con.sendall(text.encode())
        data = con.recv(SIZE)
        return pickle.loads(data)


def sendDisconnect(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        con.sendall(text.encode())
        con.close()
        return


def sendJsonFile(filePath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con.connect((HOST, PORT))
        with open(filePath, "r") as f:
            jText = f.read()

        con.sendall(jText.encode())
        data = con.recv(SIZE)
        return pickle.loads(data)
