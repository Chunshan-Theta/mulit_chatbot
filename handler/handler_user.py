from MongoDbTool.common import MongoBasicClient


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
