import pymongo
import time
class Db():
    def __init__(self):
        self.dbclient = pymongo.MongoClient('mongodb://localhost:27017/')['bigdata']
        self.usertable = self.dbclient['User'] #使用者table
        self.grouptable = self.dbclient['Group'] #群組table
        self.acttable = self.dbclient['Act'] #活動資料table
        self.inparttable = self.dbclient['InPart'] #餐與活動表table
        self.tmpacttable = self.dbclient['TmpAct'] #活動設定資料
        self.messagehistory = self.dbclient['MessageHistory'] #對話紀錄

    def isUser(self,user_id):
        search_data = {'userID':user_id}
        find_data = self.usertable.find_one(search_data)
        if find_data :
            return True
        else :
            return False
    def insertUser(self,user_id):
        insert_data = {'userID':user_id,
                        'stage':0,
                        }
        self.usertable.insert_one(insert_data)
    def isUserinGroup(self,user_id,group_id):
        search_data = {
                    'userID':user_id,
                    'groupID':group_id,
                    'stage':0,
                    }
        find_data = self.grouptable.find_one(search_data)
        if find_data :
           return True
        else :
           return False
    def insertUsertoGroup(self,user_id,group_id):
        insert_data = {
                    'userID':user_id,
                    'groupID':group_id,
                    'stage':0,
                    }
        self.grouptable.insert_one(insert_data)
    def insertActandID(self,actid,lineid,type):
        insert_data = {'actID':actid,
                        'type':type,
                        'lineid':lineid
                        }
        self.inparttable.insert_one(insert_data)
    def insertAct(self,LID,Ltype,name,date,time,place,alert_time,alert_stage):#LID = 群組ID或個人ID,Ltype = 個人或群組
        insert_data = {'actName':name,
                        'actDate':date,
                        'actTime':time,
                        'actPlace':place,
                        'actAlert':alert_time,
                        'actAlertStage':0, #0表示無
                        }
        id = self.acttable.insert(insert_data)
        self.insertActandID(id,LID,Ltype)
    def getalertAct(self):
        find_data =  {
                        'actAlert': { "$lt": int(time.time()) },
                        'actAlertStage':0,
                         }
        list_need_act = self.acttable.find(find_data)
        return list_need_act #用for 去拿資料
    def actIDtoLID(self,actid):
        find_data =  {
                        'actID':actid,
                         }
        return self.inparttable.find_one(find_data)['lineid']
    def finishAlert(self,id):
        getact = { "_id": id }
        newact = { "$set": { "actAlertStage": 1 } }
        self.acttable.update_one(getact, newact)
