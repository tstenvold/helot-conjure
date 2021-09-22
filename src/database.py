import sqlite3
from os import path
from sqlite3worker import Sqlite3Worker

DBNAME = 'pyserverless.db'


def database_start():
    if not path.isfile(DBNAME):
        initialize_DB()


def db_commit_close(con):
    con.commit()
    con.close()


def initialize_DB():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE users (userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userName text NOT NULL, authCode text NOT NULL)''')
    cur.execute(
        '''CREATE TABLE processLog (processID INTEGER NOT NULL PRIMARY KEY, userID INTEGER, state INTEGER, time date, runTime INTEGER, FOREIGN KEY(userID) REFERENCES user(userID))''')

    # only for debugging, should be removed later
    cur.execute(
        "INSERT INTO users (userName,authCode) VALUES ('tester','abc123')")
    cur.execute(
        "INSERT INTO users (userName,authCode) VALUES ('tstenvold','asdfg12345')")

    db_commit_close(con)


def list_users():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    users = cur.execute(
        'SELECT userName FROM users ORDER BY userName DESC').fetchall()
    con.close()

    print(users)


def authenticate_user(uName, aCode):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute(
        """SELECT userName , authCode FROM users WHERE userName=? AND authCode=?""", (uName, aCode))
    result = cur.fetchone()
    con.close()

    if result:
        return True

    return False
