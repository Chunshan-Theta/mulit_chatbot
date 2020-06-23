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

from handler import line_reply_handler

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
# Channel Access Token
line_bot_api = LineBotApi("T7WVBSLT4LoxIAvPQV4fQA2cJBq9OxjgLmPiOquiw6e3m8zMKHq83nuXcQ0OXaj5Z/oqni0NgPvX7r9M2MK3rhxi8ZjzTnerMywBxU7/So6AUq3YlJxQmjJd6hWBQ92avWSBLgukv3h9zxziV5wtwwdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("94e92187579a5377d59c0b936c54625f")

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if hasattr(event, 'postback'):
        app.logger.info("postback: " + str(event.postback))
        line_bot_api.push_message(event.source.user_id, TextSendMessage(text=f"我們已經收到您的要求: {event.postback}"))
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        """
        respond_text = line_reply_handler(message=event.message.text)
        message = TextSendMessage(text=respond_text)
        """
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"我們已經收到您的要求: {event.message.text}"))
        message = line_reply_handler(message=event.message.text)
        #line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(event.source.user_id, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

