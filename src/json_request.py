#!/usr/bin/env python3

import json


class json_request:
    def __init__(self, data):
        self._jsonObj = self.textToJson(data)
        self.jCode = self.jsonCode(self._jsonObj)
        self.uName = self.jsonUserName(self._jsonObj)
        self.authCode = self.jsonAuthToken(self._jsonObj)

    def jsonAuthToken(self, jsonObj):
        return jsonObj["authToken"]

    def jsonUserName(self, jsonObj):
        return jsonObj["userName"]

    def jsonCode(self, jsonObj):
        return jsonObj["Code"]

    def textToJson(self, txtjson):
        return json.loads(txtjson)
