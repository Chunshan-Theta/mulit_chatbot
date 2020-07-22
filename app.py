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
from handler.handler_line import line_reply_handler

from fb_message_bot.fb_helper import FbHelperBot

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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"我們已經收到您的要求: {event.message.text}"))
    message = line_reply_handler(message=event.message.text)
    line_bot_api.push_message(event.source.user_id, message)

# 處理Postback訊息
@handler.add(PostbackEvent)
def handle_message(event):
    app.logger.info("postback: " + str(event.postback))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"我們已經收到您的要求: {event.postback}"))


## MESSENGER
PAGE_ACCESS_TOKEN="EAAluGaMwMzwBAJjhPnmpCYrgmYHTUqTDQUF8AqzByfW35TNSmLZB3ZBRvvnXF7QShTUgGE5IBIB3b9j0Ur3RxzZAUmkhPqZCw0ESZAOFh2hdfrpNlc7QyzpUt4M2Uox3hhxSggBNgFx1QSwNOok6CoCfKrMen4ZCh7LZC1rZAXgnjFN5a5x4B0cN"
MESSENGER_AUTH_TOKEN = "messenger_auth_token"
bot = FbHelperBot(PAGE_ACCESS_TOKEN)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/messenger", methods=['GET'])
def verify():
 # Webhook verification
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

                """
                {'object': 'page', 'entry': [{'id': '108119087224240', 'time': 1595396379736, 'messaging': [{'sender': {'id': '3069312713160337'}, 'recipient': {'id': '108119087224240'}, 'timestamp': 1595396379488, 'message': {'mid': 'm_ycByns-pYXTDge2Ahgq_tK64dlW_iUMwPSiQKqTPDYSi_QK-x05ZRP4j6xZB-VuG_r9noSwhsm_X04mW6njKbQ', 'text': '搜尋:耶誕城'}}]}]}
                2020-07-22T05:39:40.067261+00:00 app[web.1]: sender_id: 3069312713160337
                
                {'object': 'page', 'entry': [{'id': '108119087224240', 'time': 1595396420065, 'messaging': [{'sender': {'id': '3069312713160337'}, 'recipient': {'id': '108119087224240'}, 'timestamp': 1595396420017, 'postback': {'title': '搜尋:耶誕城', 'payload': '搜尋:耶誕城'}}]}]}

                """
                messaging_text = None
                if "message" in messaging_event:
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                if "postback" in messaging_event:
                    if "payload" in messaging_event["postback"]:
                        messaging_text = messaging_event["postback"]["payload"]
                if messaging_text is not None:
                    try:
                        # Echo
                        if messaging_text.find("圖") != -1:
                            handler_fb.handler_pic_search(bot=bot, recipient_id=sender_id, text=messaging_text)
                        elif messaging_text.find("搜尋") != -1:
                            handler_fb.handler_pic_set_search(bot=bot, recipient_id=sender_id, text=messaging_text)
                        else:
                            response = messaging_text
                            bot.send_text_message(sender_id, f" your sender_id: {sender_id}")
                            bot.send_text_message(sender_id, messaging_text)
                    except ValueError as e:
                        bot.send_text_message(sender_id, f"對不起,我不知道你想幹嘛ＱＡＱ")
                    except Exception as e:
                        print(f"Exception: {str(e)}")
    return "ok", 200



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

