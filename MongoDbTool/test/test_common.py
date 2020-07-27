import unittest

from MongoDbTool.common import MongoBasicClient


class MyTestCase(unittest.TestCase):
    def test_something_insert(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net",db_name="MongoDbToolCommonUnittest",db_list_name="MongoDbToolCommonUnittestMainList") as db_client:
            print(db_client.query(label="unitest"))
            db_client.insert(val={"label": "unitest"})
            print(db_client.query(label="unitest"))

    def test_something_query(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net",db_name="MongoDbToolCommonUnittest",db_list_name="MongoDbToolCommonUnittestMainList") as db_client:
            print(db_client.query(label="unitest"))

    def test_something_enter_exit(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net",db_name="MongoDbToolCommonUnittest",db_list_name="MongoDbToolCommonUnittestMainList") as db_client:
            db_client.insert(val={"label": "unitest"})
            print(db_client.query(label="unitest"))

    def test_something_query_in(self):
        with MongoBasicClient(host="cluster0.enocw.mongodb.net",db_name="fbbot_like_pic",db_list_name="user_like") as db_client:
            print(db_client.query_in(shortcode=["B0yUI-njUwK","B0u5pqjn9mm","B0yUD21nh4M"]))

if __name__ == '__main__':
    unittest.main()
