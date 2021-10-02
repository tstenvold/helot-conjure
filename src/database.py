import sqlite3
from os import path
import uuid
import hashlib

import messages


class dbObj:

    def __init__(self, path):
        self.path = path

    def hash_auth(self, authCode):
        return hashlib.sha256(authCode.encode()).hexdigest()

    def initialize_DB(self, dbPath):
        con = sqlite3.connect(dbPath)
        cur = con.cursor()

        # If for some reason called with existing tables, this will delete everything! Keep your wits or lose your data
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS processLog")

        cur.execute(
            '''CREATE TABLE users (userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userName text NOT NULL, authCode text NOT NULL)''')
        cur.execute(
            '''CREATE TABLE processLog (processID STRING NOT NULL PRIMARY KEY, userID INTEGER, state STRING, starttime REAL, endtime REAL, FOREIGN KEY(userID) REFERENCES user(userID))''')

        self.db_commit_close(con)

    def add_user(self, uName, authCode):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        # Hash so that password isn't stored in plaintext in the db
        hashedAuth = self.hash_auth(authCode)
        cur.execute(
            "INSERT INTO users (userName,authCode) VALUES (?,?)", (uName, hashedAuth))
        self.db_commit_close(con)

    def del_user(self, uName):
        # needs to delete proccesses with userID
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            "DELETE FROM users WHERE userName=?", [uName])
        self.db_commit_close(con)

    def list_users(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        users = cur.execute(
            'SELECT userName FROM users ORDER BY userName DESC').fetchall()
        con.close()

        print(users)

    def get_id_user(self, uName):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(
            "SELECT userID FROM users WHERE userName=?", [uName])
        result = cur.fetchone()
        con.close()
        return result[0]

    def authenticate_user(self, uName, authCode):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        # Hash the plain text password to match the database entry
        hashedAuth = self.hash_auth(authCode)
        cur.execute(
            """SELECT userName , authCode FROM users WHERE userName=? AND authCode=?""", (uName, hashedAuth))
        result = cur.fetchone()
        con.close()

        return True if result else False

    def insert_new_proc(self, uName, sTime):
        userID = self.get_id_user(uName)
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        procID = self.generate_proc_id()
        cur.execute("INSERT INTO processLog (processID, userID, state, starttime) VALUES (?,?,?,?)",
                    (procID, userID, messages.STATE_START, sTime))

        self.db_commit_close(con)
        return procID

    def finish_proc(self, procID, fTime):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("UPDATE processLog SET state=?, endtime=? WHERE processID=?",
                    (messages.STATE_FINISHED, fTime, procID))

        self.db_commit_close(con)

    def crashed_proc(self, procID, fTime):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("UPDATE processLog SET state=?, endtime=? WHERE processID=?",
                    (messages.STATE_ERROR, fTime, procID))

        self.db_commit_close(con)

    def generate_proc_id(self):
        return uuid.uuid1().hex

    def db_commit_close(self, con):
        con.commit()
        con.close()
