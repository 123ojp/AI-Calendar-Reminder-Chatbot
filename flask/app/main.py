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
# 掃db finish


# port
port = 8000
# Flask app should start in global layout
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    print(json.dumps(req, indent=4))
    result = req.get("queryResult")
    usersay=result.get("queryText")
    intent = result.get("intent")
    parameters = result.get("parameters") # 裡面存變數 parameters.get("Bookname")
    mode = intent.get("displayName") #抓取google匹配的intent
    org_req = req.get("originalDetectIntentRequest")
    if not ( "source" in org_req and org_req.get("source") == "line"):
        return "",500
    line(org_req.get('payload'))
    if mode == 'LibraryAct':
        respone_text =  get_act()
        print ("辨別為圖書館活動")
    elif mode == "LibraryBook":
        respone_text = get_book(parameters.get("Bookname"))
        print ("辨別為圖書搜尋→",parameters.get("Bookname"))
    print ("解果:")

    #print("Response:")
    #print(fulfillmentText)
    #回傳
    res = {
        "fulfillmentText": respone_text,
        #"payload": {},
        #"outputContexts": [],
        "source": "agent"
        }

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=10000,debug=True)
    #app.run(host="0.0.0.0",port=80)
