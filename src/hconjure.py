#!/usr/bin/env python3

import sys
from optparse import OptionParser, SUPPRESS_HELP

import database
from database_admin import admin_welcome
import server
import messages


def cmd_parse(argv):

    parser = OptionParser(
        usage="usage: pyserverless.py [options]", version="%prog 0.1")

    parser.add_option("--dbadmin", dest="admin_welcome", action="store_true",
                      help="Start the database administrator")
    parser.add_option("-i", "--ip", dest="ipaddr", default='127.0.0.1',
                      help="Set the Server IP Address")
    parser.add_option("-p", "--port", dest="port", default=12345,
                      help="Set the Server Port")
    parser.add_option("-s", "--packet-size", dest="psize", default=2048,
                      help="Set the Packet Size")
    parser.add_option("-d", "--database", dest="dbpath", default="hconjure.db",
                      help="Set the database file location")
    parser.add_option("--cert", dest="certpath", default="certificate.pem",
                      help="Set the certificate file location")
    parser.add_option("--test", dest="test", action="store_true",
                      help=SUPPRESS_HELP,)

    return parser

def handle_args(argv):

    parser = cmd_parse(argv)
    options = parser.parse_args()[0]

    host = options.ipaddr
    port = int(options.port)
    size = int(options.psize)
    db = database.dbObj(options.dbpath)
    cert = options.certpath
    timeout = True if options.test else False

    if options.admin_welcome:
        admin_welcome(db)
    else:
        try:
            serv = server.serverObj(host, port, size, db, cert)
            serv.run(timeout)
        except:
            print(messages.ERROR_NODB)


if __name__ == "__main__":
    handle_args(sys.argv[1:])
