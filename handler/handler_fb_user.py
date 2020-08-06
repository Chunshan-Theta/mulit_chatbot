from MongoDbTool.common import MongoBasicClient
import json

from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack, FbButtomURL
from handler.handler_fb import basic_operation_quick_reply
from util.travel_tool import TravelUnit, new_travel_unit, add_unit_travel_units


def handler_user_like(bot, recipient_id, text):
    querys = text.split(":")
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="fbbot_like_pic",
                          db_list_name="user_like") as db_client:
        user_id = querys[1]
        shortcode = querys[2]
        db_client.insert(val={
            "user_id": user_id,
            "shortcode": shortcode
        })
    bot.send_text_message(recipient_id, f"已紀錄❤ {user_id} like {shortcode}")


def handler_user_like_all_picture(bot, recipient_id, text):
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="fbbot_like_pic",
                          db_list_name="user_like") as db_client:
        user_like_pics_shortcode_info = db_client.query(user_id=recipient_id)
        user_like_pics_shortcode_info_json = {user_like_pic_shortcode_info["shortcode"]: user_like_pic_shortcode_info for user_like_pic_shortcode_info in user_like_pics_shortcode_info}
        user_like_pics_shortcode_ids = list(user_like_pics_shortcode_info_json.keys())

        db_client.select_list("pic")
        pics = db_client.query_in(shortcode=user_like_pics_shortcode_ids)
        pics = {pic["shortcode"]:pic for pic in pics}
    pic_AttachmentGeneric_set= list()
    for k, v in user_like_pics_shortcode_info_json.items():
        pic = pics[k]
        show_code_btn_set = list()
        show_code_btn_set.append(FbButtomPostBack(payload=pic["shortcode"], title="show code"))
        show_code_btn_set.append(pic['buttons'][1])

        Element1 = AttachmentGenericPayloadElements(title=pic['title'], subtitle=pic["subtitle"], image_url=pic["image_url"],
                                                    default_url=pic["image_url"], buttons=show_code_btn_set)

        pic_AttachmentGeneric_set.append(Element1)

    AttachmentGeneric_obj = AttachmentGeneric(elements=pic_AttachmentGeneric_set)
    responds = bot.send_templete_message(recipient_id, AttachmentGeneric_obj)
    responds = bot.send_quickreplay_message(recipient_id, basic_operation_quick_reply)


def handler_user_create_travel(bot, recipient_id, text):
    query = text[text.index(":") + 1:]
    tu = TravelUnit(owner=recipient_id, title=query)
    new_travel_unit(tu)
    bot.send_text_message(recipient_id, f"已經創建行程:{query}")


def handler_user_create_travel_unit(bot, recipient_id, text):
    query = text.split(":")
    uuid = query[1]
    short_code = query[2]
    add_unit_travel_units(travel_units_uuid=uuid, shortcode=short_code)
    bot.send_text_message(recipient_id, "已成功！")