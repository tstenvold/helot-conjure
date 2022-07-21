#!/usr/bin/env python3

import os
import messages
import json
import socket
import ssl
import pickle
from PIL import Image
import urllib.request


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
SIZE = 2048

def test_basic():
    assert sendJsonFile("tests/basic.json") == 10


def test_forloop():
    assert sendJsonFile("tests/function.json") == 6

def test_function():
    code = "def xyz():\n\treturn 15\nresult = xyz()"
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": '+json.dumps(code)+'}') == 15


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
        '{"userName": "teste","authToken": "abc123","Code": "result = 2+2*4"}') is None


def test_longexec():
    assert sendString(
        '{"userName": "tester","authToken": "abc123","Code": "result=2\\nfor i in range (6,15):\\n\\tresult=result**i\\nresult= result % 10"}') == 6

def test_image_rotate():
    ssock = init_ssl_connection()
    ssock.connect((HOST, PORT))
    file = open("client/image_manipulation.py").read()

    #Get the image and rotate yourself to check the server returns the correct image
    urllib.request.urlretrieve("https://opensource.com/sites/default/files/images/jupyter-image_7_0.png", "deer.jpg")
    img = Image.open("deer.jpg")
    result = img.rotate(90)

    file = file.replace("\n", "\\n").replace('\"', '\\"')
    json = '{ "userName":"tester" ,"authToken":"abc123" ,"Code":"'+file+'"}'
    ssock.sendall(json.encode())

    data = b''
    i=0
    while True:
        chunk = ssock.recv(SIZE)
        if len(chunk) < SIZE:
            data += chunk
            break
        data += chunk
    os.remove("deer.jpg")
    assert result == pickle.loads(data)


def init_ssl_connection():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.load_default_certs()
    sock = socket.socket(socket.AF_INET)
    return context.wrap_socket(sock, server_hostname=HOST)


def sendString(text):
    ssock = init_ssl_connection()
    ssock.connect((HOST, PORT))
    ssock.sendall(text.encode())
    data = ssock.recv(SIZE)
    ssock.close()
    return pickle.loads(data)


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
    data = ssock.recv(SIZE)
    ssock.close()
    return pickle.loads(data)
