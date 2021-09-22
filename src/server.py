#!/usr/bin/env python3

import socket
import types
import selectors
import database
import serverjson
import messages

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)


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

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
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


def json_process(data):
    # necessary local initalized vars
    result = ''
    ex_locals = {}

    jsonObj = serverjson.textToJson(data)
    jCode = serverjson.jsonCode(jsonObj)
    uName = serverjson.jsonUserName(jsonObj)
    aCode = serverjson.jsonAuthToken(jsonObj)

    # TODO
    # validate JSON
    # kick off into own thread and time
    if(database.authenticate_user(uName, aCode)):
        print("\nCode:")
        print(jCode)
        try:
            exec(jCode, None, ex_locals)
            result = str(ex_locals['result'])
        except:
            result = messages.INVALIDCODE

        return result
    else:
        print(messages.INVALIDAUTH)
        return messages.INVALIDAUTH
