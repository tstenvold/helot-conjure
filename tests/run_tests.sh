#!/usr/bin/env zsh

coverage erase
coverage run -m -p pytest tests/test_database.py
coverage run -p ./src/pyserverless.py &
coverage run -p -m pytest tests/test_server_resp.py
pkill -P $$
rm test.db
coverage combine
coverage report --omit="/usr/*"