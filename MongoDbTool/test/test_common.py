import unittest

from MongoDbTool.common import MongoBasicClient


class MyTestCase(unittest.TestCase):
    def test_something_insert(self):
        db_client = MongoBasicClient(host="cluster0.enocw.mongodb.net",
                                     db_name="MongoDbToolCommonUnittest")

        db_client.select_list(name="MongoDbToolCommonUnittestMainList")
        db_client.insert(val={"label": "unitest"})
        db_client.query(search_filter={"label": "unitest"})

    def test_something_insert(self):
        db_client = MongoBasicClient(host="cluster0.enocw.mongodb.net",
                                     db_name="MongoDbToolCommonUnittest",
                                     db_list_name="MongoDbToolCommonUnittestMainList")

        db_client.select_list(name="MongoDbToolCommonUnittestMainList")
        #db_client.insert(val={"label": "unitest"})
        db_client.insert_multi(vals=[{"label": "unitest"},{"label": "unitest"}])
        db_client.query(search_filter={"label": "unitest"})

    def test_something_query(self):
        db_client = MongoBasicClient(host="cluster0.enocw.mongodb.net",
                                     db_name="MongoDbToolCommonUnittest")

        db_client.select_list(name="MongoDbToolCommonUnittestMainList")
        db_client.query(label="unitest")

    def test_something_enter_exit(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net",db_name="MongoDbToolCommonUnittest",db_list_name="MongoDbToolCommonUnittestMainList") as db_client:
            db_client.select_list(name="MongoDbToolCommonUnittestMainList")
            db_client.insert(val={"label": "unitest"})
            db_client.query(search_filter={"label": "unitest"})

if __name__ == '__main__':
    unittest.main()
