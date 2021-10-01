#!/usr/bin/env python3

from os import path
import sys
from optparse import OptionParser

import database
from database_admin import admin_welcome
from server import start_server
import messages


def cmd_parse(argv):

    parser = OptionParser(
        usage="usage: pyserverless.py [options]", version="%prog 0.1")

    parser.add_option("--dbadmin", dest="admin_welcome", action="store_true",
                      help="Start the database administrator",)
    parser.add_option("-i", "--ip", dest="ipaddr", default='127.0.0.1',
                      help="Set the Server IP Address")
    parser.add_option("-p", "--port", dest="port", default=12345,
                      help="Set the Server Port")
    parser.add_option("-s", "--packet-size", dest="psize", default=2048,
                      help="Set the Packet Size")
    parser.add_option("-d", "--database", dest="dbpath", default="pyserverless.db",
                      help="Set the database file location")

    return parser


def handle_args(argv):

    parser = cmd_parse(argv)
    options = parser.parse_args()[0]

    ipaddr = options.ipaddr
    port = options.port
    psize = options.psize
    database.DBNAME = options.dbpath

    if options.admin_welcome:
        admin_welcome()
    else:
        if not path.isfile(database.DBNAME):
            return messages.ERROR_NODB
        else:
            start_server(ipaddr, port, psize)


if __name__ == "__main__":
    handle_args(sys.argv[1:])
