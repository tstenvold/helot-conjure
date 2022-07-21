#!/usr/bin/env python3

import json


class json_request:
    def __init__(self, data):
        self._jsonObj = self.textToJson(data)
        self.jCode = self.jsonCode(self._jsonObj)
        self.uName = self.jsonUserName(self._jsonObj)
        self.authCode = self.jsonAuthToken(self._jsonObj)

    @staticmethod
    def jsonAuthToken(jsonObj):
        return jsonObj["authToken"]

    @staticmethod
    def jsonUserName(jsonObj):
        return jsonObj["userName"]

    @staticmethod
    @staticmethod
    def jsonCode(jsonObj):
        return jsonObj["Code"]

    @staticmethod
    def textToJson(txtjson):
        return json.loads(txtjson)
