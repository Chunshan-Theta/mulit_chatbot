import unittest

from MongoDbTool.common import MongoBasicClient
from util.continue_command import command_tmp_record
from util.search_pic import get_pics, pic


class MyTestCase(unittest.TestCase):
    def test_something(self):
        user_id="unittest-user"
        user_id2="unittest-user2"
        command_tmp_record.add_command(user_id=user_id,command="label1")
        self.assertEqual("label1",command_tmp_record.find_user(user_id=user_id))
        self.assertIsNone(command_tmp_record.find_user(user_id=user_id))
        command_tmp_record.add_command(user_id=user_id, command="label1")
        self.assertIsNone(command_tmp_record.find_user(user_id=user_id2))


if __name__ == '__main__':
    unittest.main()
