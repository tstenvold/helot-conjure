#!/usr/bin/env python3

import sqlite3
import time
import selectors
import types
import socket
import ssl
import os
import logging
import sys
from os import ftruncate
from json.decoder import JSONDecodeError
import pickle

import messages
from json_request import json_request
import database
import sandbox


class serverObj:

    logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

    def __init__(self, host="localhost", port=12345, size=2048, db=database.dbObj("hconjure.db"),cert="certificate.pem"):
        self.host = host
        self.port = port
        self.size = size
        self.cert = cert
        self.db = db
        if not os.path.exists(db.path):
            raise sqlite3.DatabaseError
        if not os.path.exists(cert):
            raise ssl.CertificateError

    def accept_wrapper(self, sel, sock):
        try:
            conn, addr = sock.accept()  # Should be ready to read
            logging.info('accepted connection from', addr)

            data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            sel.register(conn, events, data=data)
        except ssl.SSLError:
            logging.error(messages.SSLERROR)
            return

    def service_connection(self, sel, key, mask):
        sock = key.fileobj
        data = key.data

        try:
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(self.size)  # Should be ready to read
                if recv_data:
                    data.outb += recv_data
                else:
                    logging.info('closing connection to', data.addr)
                    sel.unregister(sock)
                    sock.close()

            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    result = self.json_process(data.outb)
                    serialized = pickle.dumps(result)
                    # TODO should give a response rather than wait for process completition
                    sent = sock.sendall(serialized)
                    # remove data from output when result is sent
                    data.outb = ''

        except:
            logging.error(messages.CONNERROR)

    def server_timeout(self, test,timeout):
        if test and time.time() - timeout >= 3:
            return False
        else:
            return True

    def run(self,tout=False):

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert, keyfile=self.cert)
        
        sel = selectors.DefaultSelector()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            logging.info('listening on', (self.host, self.port))

            with context.wrap_socket(sock, server_side=True) as ssock:
                sel.register(ssock, selectors.EVENT_READ, data=None)

                ltime = time.time()
                while self.server_timeout(tout,ltime):
                    
                    events = sel.select(timeout=1 if tout else None)
                    for key, mask in events:
                        if key.data is None:
                            self.accept_wrapper(sel, key.fileobj)
                        else:
                            self.service_connection(sel, key, mask)
                            ltime = time.time()

    def json_process(self, data):

        try:
            request = json_request(data)
        except JSONDecodeError:
            return messages.INVALIDJSON

        if self.db.authenticate_user(request.uName, request.authCode):

            sTime = time.time()
            procID = self.db.insert_new_proc(request.uName, sTime)
            result = sandbox.run_code(request.jCode)
            fTime = time.time()

            if result == messages.INVALIDCODE:
                self.db.crashed_proc(procID, fTime)
            else:
                self.db.finish_proc(procID, fTime)
        else:
            result = messages.INVALIDAUTH

        return result