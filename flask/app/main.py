# -*- coding: utf-8 -*-
##### import urllib
import json
import os
import db,fun
from flask import Flask
from flask import request
from flask import make_response
import threading,time,requests


## 主動發line
def sendLine(user, text):
    TOKEN = "oVbjOkF5o5/nAz2dR2kUiVCldSEoPrcU+ZMUGfEM78BOkb7B6/Oww3obdTV/OelA1c7DTcHYzrnl964n1gjrTRIxhgykWRE5Frwfn7rk2Lb//Zd+dBUiVzIn51dcQD6J+uGRZ0IX4WQN47YxUMF5AAdB04t89/1O/w1cDnyilFU="
    LINE_API = 'https://api.line.me/v2/bot/message/push'
    CHANNEL_SERECT ='Bearer {"'+TOKEN+'"}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': CHANNEL_SERECT
    }

    data = json.dumps({
        "to": user,
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
# 拿
funt = fun.Fun()

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
    print(req)
    result = req.get("queryResult")
    usersay=result.get("queryText")
    intent = result.get("intent")
    parameters = result.get("parameters") # 裡面存變數 parameters.get("Bookname")
    mode = intent.get("displayName") #抓取google匹配的intent
    org_req = req.get("originalDetectIntentRequest")
    if not ( "source" in org_req and org_req.get("source") == "line"):
        return "",500
    room_type = org_req.get('payload').get('data').get('source').get('type')
    room_type_n = -1
    if room_type == "group":
        room_type_n = 1
    if room_type == "user":
        room_type_n = 0
    LID = funt.getLine(org_req)
#    line(org_req.get('payload'))
    if mode == 'createActEasy':
        act,date,time,place,unix_time = funt.getActItem(parameters,org_req)
        mongodb.insertAct(LID,room_type_n,act,date,time,place,unix_time)
        respone_text =  "建立成功\n"+"活動："+act+"\n"+date+" "+time+place
        print ("辨別為一般建立")
    if mode.find('make') == 0:
        if not(mongodb.isSettingTmpAct(LID)):
            mongodb.setTmpActSate(LID)
        if mode == "makeActName":
            mongodb.setTmpActName(LID,parameters.get('name'))
        if mode == "makeActDate":
            date = parameters.get('date')
            date_re = re.search('([0-9]{4})-([0-9]{2})-([0-9]{2})',date)
            year = int(date_re.group(1))
            month = int(date_re.group(2))
            day = int(date_re.group(3))
            date = str(year)+"年"+str(month)+"月"+str(day)+"日"
            mongodb.setTmpActDate(date)
        if mode == "makeActTime":
            time = parameters.get('time')
            time_re = re.search('([0-9]{1,2})[^\d]+([0-9]{1,2})',time)
            hour = int(time_re.group(1))
            min = int(time_re.group(2))
            time = str(hour)+":"+str(min)
            mongodb.setTmpActTime(time)
        if mode == "makeActPlace":
            mongodb.setTmpActPlace(LID,parameters.get('place'))
        tmpAct = mongodb.getTmpActAlert(LID)
        respone_text = "活動\n 名稱：{}\n 日期：{}\n 時間：{}\n 地點：{}".format(tmpAct['actName'],tmpAct['actDate'],tmpAct['actTime'],tmpAct['actPlace'])
        if mongodb.readyTmpAct(LID):
            respone_text += "\n是否確定建立活動?"
    if mode == "tmpActGo":
        if mongodb.readyTmpAct(LID):
            tmpAct = mongodb.getTmpActAlert(LID)
            time_re = re.search('([0-9]{1,2}):([0-9]{1,2})',tmpAct['actTime'])
            hour = int(time_re.group(1))
            min = int(time_re.group(2))
            date_re = re.search('([0-9]{4})年([0-9]{2})月([0-9]{2})',tmpAct['actDate'])
            year = int(date_re.group(1))
            month = int(date_re.group(2))
            day = int(date_re.group(3))
            unix_time = datetime.datetime(year,month,day,hour,min).timestamp()
            mongodb.setTmpActAlert(unix_time)
            respone_text = "活動\n 名稱：{}\n 日期：{}\n 時間：{}\n 地點：{}\n建立成功".format(tmpAct['actName'],tmpAct['actDate'],tmpAct['actTime'],tmpAct['actPlace'])
        else :
            return

    #
    # elif mode == "LibraryBook":
    #     respone_text = get_book(parameters.get("Bookname"))
    #     print ("辨別為圖書搜尋→",parameters.get("Bookname"))
    print ("解果:")

    #print("Response:")
    #print(fulfillmentText)
    #回傳
    res = {
        "fulfillmentText": respone_text,
        "source": "agent"
        }

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=10000,debug=True)
    app.run(host="0.0.0.0",port=80)