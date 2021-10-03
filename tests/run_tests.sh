#!/usr/bin/env zsh

coverage erase
coverage run -a -m pytest tests/test_database.py
coverage run -a ./src/pyserverless.py -d test.db & coverage run -a -m pytest tests/test_server_resp.py
pkill -P $$
rm test.db
coverage combine
coverage html --omit="/usr/*"
coverage report --omit="/usr/*"