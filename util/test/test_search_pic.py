import unittest

from MongoDbTool.common import MongoBasicClient
from util.search_pic import get_pics, pic


class MyTestCase(unittest.TestCase):
    def test_something_get_pic(self):
        print(get_pics())

    def test_something_pic(self):
        pic(title="hi", media="https://....", url="https://")

if __name__ == '__main__':
    unittest.main()
