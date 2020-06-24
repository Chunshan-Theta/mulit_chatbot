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
# Channel Access Token
line_bot_api = LineBotApi(Channel_Access_Token)
# Channel Secret
handler = WebhookHandler(Channel_Secret)

Line_test_bot_user_id = "Udeadbeefdeadbeefdeadbeefdeadbeef"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

