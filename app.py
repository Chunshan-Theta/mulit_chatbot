import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import logging

from handler import handler_fb
from config import Channel_Access_Token, Channel_Secret
from handler.handler_fb import basic_operation_quick_reply
from handler.handler_line import line_reply_handler

from fb_message_bot.fb_helper import FbHelperBot
from handler.handler_fb_user import handler_user_like,handler_user_like_all_picture
from line_bot.line_helper import LineBot
import json

from util.continue_command import command_tmp_record

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

## LINE
# Channel Access Token
line_bot_api = LineBotApi(Channel_Access_Token)

# Channel Secret
handler = WebhookHandler(Channel_Secret)

Line_test_bot_user_id = "Udeadbeefdeadbeefdeadbeefdeadbeef"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/line", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("line Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理message訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id == Line_test_bot_user_id:
        return
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"使用者{event.source.user_id}您好, 我們已經收到您的要求: {event.message.text}"))
    line_bot = LineBot(Channel_Access_Token)
    line_reply_handler(bot=line_bot,recipient_id=event.source.user_id,message=event.message.text)
    #line_bot_api.push_message(event.source.user_id, message)

# 處理Postback訊息
@handler.add(PostbackEvent)
def handle_message(event):
    app.logger.info("postback: " + str(event.postback))
    return_str = json.loads(str(event.postback))["data"]
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"我們已經收到您的要求: {return_str}"))


## MESSENGER
PAGE_ACCESS_TOKEN="EAAluGaMwMzwBAJjhPnmpCYrgmYHTUqTDQUF8AqzByfW35TNSmLZB3ZBRvvnXF7QShTUgGE5IBIB3b9j0Ur3RxzZAUmkhPqZCw0ESZAOFh2hdfrpNlc7QyzpUt4M2Uox3hhxSggBNgFx1QSwNOok6CoCfKrMen4ZCh7LZC1rZAXgnjFN5a5x4B0cN"
MESSENGER_AUTH_TOKEN = "messenger_auth_token"
bot = FbHelperBot(PAGE_ACCESS_TOKEN)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/messenger", methods=['GET'])
def verify():
 # Webhook verification
    if "hub.challenge" in request.args:
        return request.args["hub.challenge"], 200
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == MESSENGER_AUTH_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200



@app.route("/callback/messenger", methods=['POST'])
def webhook():
    data = request.get_json()
    #print(f"data: {data}")
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                print(f"sender_id: {sender_id}")

                messaging_text = None
                if "message" in messaging_event:
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                if "postback" in messaging_event:
                    if "payload" in messaging_event["postback"]:
                        messaging_text = messaging_event["postback"]["payload"]
                if messaging_text is not None:

                    continue_command =  command_tmp_record.find_user(user_id=sender_id)
                    if continue_command is not None:
                        if continue_command == "我想搜尋":
                            messaging_text = "搜尋:"+messaging_text

                    #
                    try:
                        if messaging_text.find("圖") != -1:
                            handler_fb.handler_pic_search(bot=bot, recipient_id=sender_id, text=messaging_text)
                        elif messaging_text.find("搜尋") != -1:
                            handler_fb.handler_pic_set_search(bot=bot, recipient_id=sender_id, text=messaging_text)
                        elif messaging_text.find("LIKES_PIC") != -1:
                            handler_user_like(bot=bot, recipient_id=sender_id, text=messaging_text)
                        elif messaging_text.find("我的最愛") != -1:
                            handler_user_like_all_picture(bot=bot, recipient_id=sender_id, text=messaging_text)
                        elif messaging_text.find("我想搜尋相關圖像") != -1:
                            command_tmp_record.add_command(user_id=sender_id, command="我想搜尋")
                            bot.send_text_message(sender_id, f"請問你想搜尋什麼圖像呢?")
                        else:
                            bot.send_text_message(sender_id, f"your id: {sender_id}")
                            bot.send_quickreplay_message(sender_id, basic_operation_quick_reply)

                    except ValueError as e:
                        print(f"ValueError: {e},{messaging_text}")
                        bot.send_text_message(sender_id, f"對不起,我不知道你想幹嘛ＱＡＱ")
                    except Exception as e:
                        print(f"Exception: {str(e)}")
    return "ok", 200



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

