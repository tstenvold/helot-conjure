#!/usr/bin/env python3

import time
import messages
import serverjson
import database
import selectors
import types
import socket
from RestrictedPython import compile_restricted_exec
from os import ftruncate
from json.decoder import JSONDecodeError


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
PSIZE = 2048        # Standard size of data to be send / recieved


def accept_wrapper(sel, sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(sel, key, mask):
    sock = key.fileobj
    data = key.data

    try:
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(PSIZE)  # Should be ready to read
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
                data.outb = ''

    except:
        print(messages.CONNERROR)


def start_server():
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print('listening on', (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    while True:

        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel, key.fileobj)
            else:
                service_connection(sel, key, mask)


def exec_sandbox(jCode):
    result = ''
    ex_locals = {}
    try:
        byte_code = compile(jCode, filename='<inline code>', mode='exec')
        exec(byte_code, None, ex_locals)
        result = str(ex_locals['result'])
    except:
        result = messages.INVALIDCODE

    return result


def json_process(data):

    try:
        request = serverjson.jsonRequest(data)
    except JSONDecodeError:
        return messages.INVALIDJSON

    if(database.authenticate_user(request.uName, request.aCode)):

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
