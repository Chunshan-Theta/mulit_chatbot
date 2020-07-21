from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult
import datetime

class MongoBasicClient:
    def __init__(self, host, db_name, db_list_name="customers"):
        self.user = "pythontest"
        self.password = "pythontest"
        self.host = host
        self.db_name = db_name
        self.ObjClient = MongoClient(host=f"mongodb+srv://{self.user}:{self.password}@{host}/{db_name}?retryWrites=true&w=majority")
        self.SelectedDB = self.ObjClient[db_name]
        self.SelectedList = self.SelectedDB[db_list_name]
        self._date_fmt = "%Y/%m/%d %H:%M:%S"

    def change_user(self,account,pws):
        self.user = account
        self.password = pws
        self.ObjClient = MongoClient(host=f"mongodb+srv://{self.user}:{self.password}@{self.host}/{self.db_name}?retryWrites=true&w=majority")

    def select_list(self,name):
        self.SelectedList = self.SelectedDB[name]

    def insert(self, val: dict):
        default = {
            "created": datetime.datetime.now().strftime(self._date_fmt),
            "updated": datetime.datetime.now().strftime(self._date_fmt)
        }
        val.update(default)
        insert_result: InsertOneResult = self.SelectedList.insert_one(val)
        return insert_result


    def query(self,projection: dict = None, **kwargs):
        if projection is None:
            for x in self.SelectedList.find(filter= kwargs):
                print(x)
        else:
            for x in self.SelectedList.find(filter= kwargs, projection=projection):
                print(x)

