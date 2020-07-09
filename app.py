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

from config import Channel_Access_Token, Channel_Secret
from handler import line_reply_handler

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
from pymessenger import Bot
PAGE_ACCESS_TOKEN="EAAIXsvACy2QBAOZBOdvLVGTOQ2NNZBYNCe94g4qWylFYguZCu9H6oov2xXKpDkMhZBgRZC94kVnY8AhXCaZCXGdJ95ezWvvo9BtQcL7SHSDrZCJB60HBZAa2VZAFqXVPnA8gVrZAPKDdsMQirqAB2u13EZCkyqDJbZBHHDrHODVHl0oWPaZBBE1h7Jl5O"
MESSENGER_AUTH_TOKEN = "messenger_auth_token"
bot = Bot(PAGE_ACCESS_TOKEN)

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
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                print(f"sender_id: {sender_id}")


                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                    # Echo
                    response = messaging_text
                    bot.send_text_message(sender_id, messaging_text)
    return "ok", 200



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

