#!/usr/bin/env python3

from database import database_start
from server import start_server


# initialized DB if it doesn't exist
database_start()
start_server()
