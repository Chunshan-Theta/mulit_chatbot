import json

from MongoDbTool.common import MongoBasicClient
from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack,FbButtomURL
from util.search_pic import get_pics, get_a_pic, pic_set_obj


def handler_user_like(bot,recipient_id,text):
    querys = text.split(":")
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="fbbot_like_pic",
                          db_list_name="user_like") as db_client:
        user_id = querys[1]
        shortcode = querys[2]
        db_client.insert(val={
            "user_id": user_id,
            "shortcode": shortcode
        })
    bot.send_text_message(recipient_id, f"已紀錄❤")
