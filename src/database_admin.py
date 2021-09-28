#!/usr/bin/env python3

import sqlite3
from os import path
import uuid
import database
from messages import *
from sqlite3worker import Sqlite3Worker


def database_admin_welcome():
    print("")
    print(DBA_WELCOME)
    db_command()


def db_command():
    print("")
    switcher = {
        '1': add_user,
        '2': del_user,
        '3': init_db,
        'q': quit
    }
    opt = input(DBA_COMMANDS)
    func = switcher.get(opt, lambda: db_command)
    print("")
    func()


def get_name():
    return input(DBA_NAME)


def init_db():
    database.initialize_DB()
    print(DBA_INIT)
    db_command()


def add_user():
    uName = get_name()
    authCode = input(DBA_AUTH)
    database.add_user(uName, authCode)
    print(DBA_ADDED, uName)
    db_command()


def del_user():
    uName = get_name()
    database.del_user(uName)
    print(DBA_DELETED, uName)
    db_command()


database_admin_welcome()
