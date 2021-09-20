#!/usr/bin/env python3

import json


def textToJson(txtjson):
    return json.loads(txtjson)


def jsonAuthToken(jsonObj):
    return jsonObj["authToken"]


def jsonCode(jsonObj):
    return jsonObj["Code"]
