import pymongo
import time
class Db():
    def __init__(self):
        self.dbclient = pymongo.MongoClient('mongodb://db:27017/')['bigdata']
        self.usertable = self.dbclient['User'] #使用者table
        self.grouptable = self.dbclient['Group'] #群組table
        self.acttable = self.dbclient['Act'] #活動資料table
        self.inparttable = self.dbclient['InPart'] #餐與活動表table
        self.tmpacttable = self.dbclient['TmpAct'] #活動設定資料
        self.messagehistory = self.dbclient['MessageHistory'] #對話紀錄
    def insertMessage(self,user_id,data):
        insert_data = {'userID':user_id,
                      'message':data,
                      }
        self.messagehistory.insert_one(insert_data)
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
    def insertAct(self,LID,Ltype,name,date,time,place,alert_time):#LID = 群組ID或個人ID,Ltype = 個人或群組
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
    def searchAct(self,id): #請給提醒ID
        list_id = self.searchActid(id)
        list_act = []
        for tmpid in list_id:           
            find_data =  {
                            '_id': tmpid['actID'],
                             }
            list_act.append(self.acttable.find(find_data))
        return list_act #用for 去拿資料
    def searchActid(self,id): #請給提醒ID
        find_data =  {
                        'lineid': id,
                         }
        list_id = self.inparttable.find(find_data)        
        return list_id #用for 去拿資料
    def delAct(self,id):
        find_data =  {
                        '_id': id,
                         }
        self.acttable.delete_one(find_data)
        find_data =  {
                        'actID': id,
                         }
        self.inparttable.delete_one(find_data)
    def isSettingTmpAct(self,id):
        search_data = {
                    'lineid':id,
                    }
        find_data = self.tmpacttable.find_one(search_data)
        if find_data :
           return True
        else :
           return False
    def setTmpActSate(self,id):
       insert_data = {
                       'actName':"NULL",
                       'actDate':"NULL",
                       'actTime':"NULL",
                       'actPlace':"NULL",
                       'actAlert':0,
                       'actAlertStage':0,
                       'Scode':1,
                       'lineid':id,
                       }
       self.tmpacttable.insert_one(insert_data)
    def setTmpActName(self,line_id,name):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        Scode = find_data['Scode'] | 2**1
        newact = { "$set": { "actName": name, "Scode":Scode } }
        self.tmpacttable.update_one(getact, newact)
    def setTmpActDate(self,line_id,date):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        Scode = find_data['Scode'] | 2**2
        newact = { "$set": { "actDate": date, "Scode":Scode } }
        self.tmpacttable.update_one(getact, newact)
    def setTmpActTime(self,line_id,time):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        Scode = find_data['Scode'] | 2**3
        newact = { "$set": { "actTime": time, "Scode":Scode } }
        self.tmpacttable.update_one(getact, newact)
    def setTmpActPlace(self,line_id,place):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        Scode = find_data['Scode'] | 2**4
        newact = { "$set": { "actPlace": place, "Scode":Scode } }
        self.tmpacttable.update_one(getact, newact)
    def setTmpActAlert(self,line_id,alert):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        Scode = find_data['Scode'] | 2**5
        newact = { "$set": { "actAlert": alert, "Scode":Scode } }
        self.tmpacttable.update_one(getact, newact)
    def readyTmpAct(self,line_id):
        getact = { "lineid": line_id }
        find_data = self.tmpacttable.find_one(getact)
        if find_data['Scode'] == 31:
            return True
        else:
            return False
    def getTmpAct(self,line_id):
        getact = { "lineid": line_id }
        return self.tmpacttable.find_one(getact)
    def delTmpAct(self,id):
        find_data =  {
                        'lineid': id,
                         }
        self.tmpacttable.delete_one(find_data)
        
    def searchActDate(self,id,date): #請給提醒ID
        list_id = self.searchActid(id)
        list_act = []
        for tmpid in list_id:           
            find_data =  {
                            '_id': tmpid['actID'],
                            }
            list_act.append(self.acttable.find(find_data))
            
        temp = []
        for tmpAct in list_act:
            if(date in tmpAct['actDate']):
                temp.append(tmpAct)
        return temp #用for 去拿資料
