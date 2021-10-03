#!/usr/bin/env python3

import os
import database
import database_admin
from faker import Faker
import time
import random
import pyserverless
import messages
fake = Faker()

dbpath = "test.db"
db = database.dbObj(dbpath)

def gen_fake_users():
    users = []
    Faker.seed(time.time())
    for i in range(100):
        users.append((fake.first_name(),fake.ssn()))
    
    return users

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

def test_add_tester():
    #user important for server tests
    db.add_user("tester","abc123")
    assert db.authenticate_user("tester","abc123") == True

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