#!/usr/bin/env python3

import sqlite3
from sqlite3worker import Sqlite3Worker

DBNAME = 'pyserverless.db'


def dbCommitClose(con):
    con.commit()
    con.close()


def initializeDB():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE users (userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userName text NOT NULL, authCode text NOT NULL)''')
    cur.execute(
        "INSERT INTO users (userName,authCode) VALUES ('tester','abc123')")
    cur.execute(
        "INSERT INTO users (userName,authCode) VALUES ('tstenvold','asdfg12345')")

    dbCommitClose(con)


def listOfUsers():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    users = cur.execute(
        'SELECT userName FROM users ORDER BY userName DESC').fetchall()
    con.close()

    print(users)


def authenticate(uName, aCode):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute(
        """SELECT userName , authCode FROM users WHERE userName=? AND authCode=?""", (uName, aCode))
    result = cur.fetchone()
    con.close()

    if result:
        return True

    return False
