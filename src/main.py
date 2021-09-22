#!/usr/bin/env python3

from database import databaseStart
from server import startServer


# initialized DB if it doesn't exist
databaseStart()
startServer()
