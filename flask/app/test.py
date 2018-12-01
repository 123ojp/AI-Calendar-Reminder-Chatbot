import db
a = db.Db()
# a.insertUser("aa")
# print(a.isUser("aa"))
# print(a.isUser("b"))
# a.insertUsertoGroup("aa","dd")
# print(a.isUserinGroup("aa","ddd"))
#
a.insertAct("LID","Ltype","name","date","time","place",1,"alert_stage")
# a.alertAct()
# -*- coding: utf-8 -*-
##### import urllib
import json
import os
import db
from flask import Flask
from flask import request
from flask import make_response
import threading,time,requests

## 主動發line
def sendLine(user, text):
    TOKEN = "oVbjOkF5o5/nAz2dR2kUiVCldSEoPrcU+ZMUGfEM78BOkb7B6/Oww3obdTV/OelA1c7DTcHYzrnl964n1gjrTRIxhgykWRE5Frwfn7rk2Lb//Zd+dBUiVzIn51dcQD6J+uGRZ0IX4WQN47YxUMF5AAdB04t89/1O/w1cDnyilFU="
    LINE_API = 'https://api.line.me/v2/bot/message/multicast'
    CHANNEL_SERECT ='Bearer {"'+TOKEN+'"}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': CHANNEL_SERECT
    }

    data = json.dumps({
        "to": [user],
        "messages":[
        {
            "type":"text",
            "text":text
        }
        ]
    })
    r = requests.post(LINE_API, headers=headers, data=data)
    print(user, text)

# 掃db
mongodb = db.Db()
def routine():
    while True:
        for act in mongodb.getalertAct():
            print(act['_id'])
            lineid = mongodb.actIDtoLID(act['_id'])
            text = "行事曆提醒："+act['actName']+"\n時間："+act["actDate"]+act['actTime']
            sendLine(lineid, text)
            mongodb.finishAlert(act['_id'])
        time.sleep(1)

t = threading.Thread(target = routine)
t.start()
# {
#     "responseId": "wwww1",
#     "queryResult": {
#         "queryText": "\u7684",
#         "action": "input.unknown",
#         "parameters": {},
#         "allRequiredParamsPresent": true,
#         "intent": {
#             "name": "wwwwa",
#             "displayName": "Default Fallback Intent",
#             "isFallback": true
#         },
#         "intentDetectionConfidence": 1.0,
#         "languageCode": "zh-cn"
#     },
#     "originalDetectIntentRequest": {
#         "source": "line",
#         "payload": {
#             "data": {
#                 "replyToken": "wwww",
#                 "source": {
#                     "groupId": "www",
#                     "type": "group",
#                     "userId": "www"
#                 },
#                 "message": {
#                     "text": "\u7684",
#                     "id": "8943853922878",
#                     "type": "text"
#                 },
#                 "type": "message",
#                 "timestamp": 1543676963187.0
#             },
#             "source": "line"
#         }
#     },
#     "session": "pwwww-473cdc82c02c"
# }
