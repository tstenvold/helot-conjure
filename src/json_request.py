#!/usr/bin/env python3

import json


class json_request:
    def __init__(self, data):
        self.__jsonObj = self.textToJson(data)
        self.jCode = self.jsonCode(self.jsonObj)
        self.uName = self.jsonUserName(self.jsonObj)
        self.aCode = self.jsonAuthToken(self.jsonObj)

    def jsonAuthToken(self, jsonObj):
        return jsonObj["authToken"]

    def jsonUserName(self, jsonObj):
        return jsonObj["userName"]

    def jsonCode(self, jsonObj):
        return jsonObj["Code"]

    def textToJson(self, txtjson):
        return json.loads(txtjson)
