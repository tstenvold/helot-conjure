#!/usr/bin/env python3

import os
import database
import database_admin as dbadmin
from faker import Faker
import time
import random
import messages
import server
import pytest
import ssl
import sqlite3


fake = Faker()

dbpath = "test.db"
db = database.dbObj(dbpath)

def gen_fake_users():
    users = []
    Faker.seed(time.time())
    for i in range(100):
        users.append((fake.first_name(),fake.ssn()))
    
    return users

def test_no_db():
    nodb = database.dbObj("nodb.db")
    with pytest.raises(sqlite3.DatabaseError):
        server.serverObj("localhost", 12345, 2048, nodb, "certificate.pem")

def test_no_cert():
    #ensure the cert doesn't exist
    certPath = "nocert.pem"
    if os.path.isfile(certPath):
        os.remove(certPath)
    
    with pytest.raises(ssl.CertificateError):
        server.serverObj("localhost", 12345, 2048, db, certPath) == ssl.CertificateError

def test_createdb():
    db.initialize_DB(db.path)
    assert os.path.isfile(dbpath)

def test_insert_users():
    fusers = gen_fake_users()
    for i in fusers:
        db.add_user(i[0],i[1])
    
    for i in range(3):
        n = random.randint(0,99)
        assert db.authenticate_user(fusers[n][0], fusers[n][1]) == True
        assert db.authenticate_user(fusers[n][1], fusers[n][0]) == False

    assert len(db.list_users()) == 100

def test_delete_users():
    users = db.list_users()
    deluser = []
    for i in range(50):
        n = random.randint(0,99)
        deluser.append(users[n][0])
        db.del_user(users[n][0])
    
    nusers = db.list_users()
    for name, in nusers:
        assert name not in deluser

def test_add_tester():
    #user important for server tests
    db.add_user("tester","abc123")
    assert db.authenticate_user("tester","abc123") == True

def run_db_admin_inputs(capsys,input_values):
    def mock_input(s):
        return input_values.pop(0)

    dbadmin.input = mock_input

    with pytest.raises(SystemExit):
        dbadmin.admin_welcome(db)

    return capsys.readouterr()

def test_db_admin_add_user(capsys):
    input_values = ['1', 'tester123', 'password' , "q"]
    lenbefore = len(db.list_users())
    out, err = run_db_admin_inputs(capsys,input_values)
    lenafter = len(db.list_users())

    assert db.authenticate_user("tester123","password") == True
    assert lenafter == lenbefore+1

def test_db_admin_del_user(capsys):

    input_values = ['2', 'tester123' , "q"]
    lenbefore = len(db.list_users())
    out, err = run_db_admin_inputs(capsys,input_values)
    lenafter = len(db.list_users())

    assert db.authenticate_user("tester123","password") == False
    assert lenafter == lenbefore-1

    