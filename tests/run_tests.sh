#!/usr/bin/env zsh

coverage erase
coverage run -m -p pytest tests/test_database.py
coverage run -p ./src/hconjure.py --test -d test.db --cert localhost.pem &
coverage run -p -m pytest -n 5 tests/test_server.py
rm test.db
sleep 5
coverage combine
coverage report --omit="/usr/*"
coverage html --omit="/usr/*"