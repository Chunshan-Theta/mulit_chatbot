import unittest

from line_bot.line_helper import LineBot
from line_bot.line_templete import ImageCarouselElement_demo1,CardCarouselElement_domo1

PAGE_ACCESS_TOKEN = "EAAluGaMwMzwBAJjhPnmpCYrgmYHTUqTDQUF8AqzByfW35TNSmLZB3ZBRvvnXF7QShTUgGE5IBIB3b9j0Ur3RxzZAUmkhPqZCw0ESZAOFh2hdfrpNlc7QyzpUt4M2Uox3hhxSggBNgFx1QSwNOok6CoCfKrMen4ZCh7LZC1rZAXgnjFN5a5x4B0cN"
pokemon1 = "https://imgur.dcard.tw/LZNvZJ8.png"
pokemon2 = "https://imgur.dcard.tw/e7RFXhu.png"
recipient_id = "U43525d4a2e00f3613338c5c54d38a07e"
black_man_pic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s"


class MyTestCase(unittest.TestCase):
    def test_text_msg(self):
        bot = LineBot(PAGE_ACCESS_TOKEN)
        bot._push_text_message(recipient_id=recipient_id,messages=["hi","早安"])

    def test_pic_msg(self):
        bot = LineBot(PAGE_ACCESS_TOKEN)
        bot._push_a_picture(recipient_id=recipient_id,original_content_url=pokemon2,preview_image_url=pokemon1)

    def test_carousel_pic(self):
        bot = LineBot(PAGE_ACCESS_TOKEN)
        bot._push_carousel_picture(recipient_id=recipient_id, default_text="黑人問號圖組", images=[ImageCarouselElement_demo1]*3)
    def test_carousel_card(self):
        bot = LineBot(PAGE_ACCESS_TOKEN)
        bot._push_carousel_card(recipient_id=recipient_id, default_text="黑人問號圖組", cards=[CardCarouselElement_domo1]*5)

if __name__ == '__main__':
    unittest.main()
