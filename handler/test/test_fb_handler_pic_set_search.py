import unittest

from handler.handler_fb import handler_pic_set_search


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(handler_pic_set_search(bot=None,recipient_id=None,text="搜尋:台北"))


if __name__ == '__main__':
    unittest.main()
