#!/usr/bin/env python3

import sqlite3
from os import path
import uuid

import database
from messages import *


def admin_welcome(dbObj):
    print("")
    print(DBA_WELCOME)
    db_command(dbObj)


def db_command(dbObj):
    print("")
    switcher = {
        '1': add_user,
        '2': del_user,
        '3': init_db,
        'q': quit_gracefully
    }
    opt = input(DBA_COMMANDS)
    func = switcher.get(opt, db_command)

    print("")
    func(dbObj)

    # loop the command prompt
    db_command(dbObj)


def quit_gracefully(dbObj):
    quit()


def get_name():
    return input(DBA_NAME)


def init_db(dbObj):
    dbObj.initialize_DB(dbObj.path)
    print(DBA_INIT)


def add_user(dbObj):
    uName = get_name()
    authCode = input(DBA_AUTH)
    dbObj.add_user(uName, authCode)
    print(DBA_ADDED, uName)


def del_user(dbObj):
    uName = get_name()
    dbObj.del_user(uName)
    print(DBA_DELETED, uName)
