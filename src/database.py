import sqlite3
from os import path
import uuid

import messages

DBNAME = 'pyserverless.db'


def db_commit_close(con):
    con.commit()
    con.close()


def initialize_DB():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS processLog")

    cur.execute(
        '''CREATE TABLE users (userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userName text NOT NULL, authCode text NOT NULL)''')
    cur.execute(
        '''CREATE TABLE processLog (processID STRING NOT NULL PRIMARY KEY, userID INTEGER, state STRING, starttime REAL, endtime REAL, FOREIGN KEY(userID) REFERENCES user(userID))''')

    db_commit_close(con)


def add_user(uName, authCode):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (userName,authCode) VALUES (?,?)", (uName, authCode))
    db_commit_close(con)


def del_user(uName):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(
        "DELETE FROM users WHERE userName=?", [uName])
    db_commit_close(con)


def list_users():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    users = cur.execute(
        'SELECT userName FROM users ORDER BY userName DESC').fetchall()
    con.close()

    print(users)


def get_id_user(uName):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(
        "SELECT userID FROM users WHERE userName=?", [uName])
    result = cur.fetchone()
    con.close()
    return result[0]


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


def insert_new_proc(uName, sTime):
    userID = get_id_user(uName)
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    procID = generate_proc_id()
    cur.execute("INSERT INTO processLog (processID, userID, state, starttime) VALUES (?,?,?,?)",
                (procID, userID, messages.STATE_START, sTime))

    db_commit_close(con)
    return procID


def finish_proc(procID, fTime):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute("UPDATE processLog SET state=?, endtime=? WHERE processID=?",
                (messages.STATE_FINISHED, fTime, procID))

    db_commit_close(con)


def crashed_proc(procID, fTime):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute("UPDATE processLog SET state=?, endtime=? WHERE processID=?",
                (messages.STATE_ERROR, fTime, procID))

    db_commit_close(con)


def generate_proc_id():
    return uuid.uuid1().hex
