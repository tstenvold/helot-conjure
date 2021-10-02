#!/usr/bin/env python3

import time
import selectors
import types
import socket
import ssl
from RestrictedPython import compile_restricted, utility_builtins
from os import ftruncate
from json.decoder import JSONDecodeError
import certifi

import messages
from json_request import json_request
import database

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="localhost.pem", keyfile="localhost.pem")

def accept_wrapper(sel, sock):
    try:
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
    except ssl.SSLError:
        print(messages.SSLERROR)
        return


def service_connection(sel, key, mask, psize):
    sock = key.fileobj
    data = key.data

    try:
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(psize)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.outb:
                result = json_process(data.outb)
                # TODO should give a response rather than wait for process completition
                sent = sock.send(result.encode())
                # remove data from output when result is sent
                data.outb = ''

    except:
        print(messages.CONNERROR)


def start_server(ip, port, psize):

    sel = selectors.DefaultSelector()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((ip, port))
        sock.listen(5)
        print('listening on', (ip, port))

        with context.wrap_socket(sock, server_side=True) as ssock:

            sel.register(ssock, selectors.EVENT_READ, data=None)

            while True:
                events = sel.select(timeout=None)

                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(sel, key.fileobj)
                    else:
                        service_connection(sel, key, mask, psize)


def exec_sandbox(jCode):
    result = ''
    ex_locals = {}
    try:
        byte_code = compile(
            jCode, filename='<inline code>', mode='exec')
        exec(byte_code, None, ex_locals)
        result = str(ex_locals['result'])
    except:
        result = messages.INVALIDCODE

    return result


def json_process(data):

    try:
        request = json_request(data)
    except JSONDecodeError:
        return messages.INVALIDJSON

    if database.authenticate_user(request.uName, request.authCode):

        sTime = time.time()
        procID = database.insert_new_proc(request.uName, sTime)
        result = exec_sandbox(request.jCode)
        fTime = time.time()

        if result == messages.INVALIDCODE:
            database.crashed_proc(procID, fTime)
        else:
            database.finish_proc(procID, fTime)
    else:
        result = messages.INVALIDAUTH

    return result
