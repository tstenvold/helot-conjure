#!/usr/bin/env zsh

./src/pyserverless.py & pytest
pkill -P $$