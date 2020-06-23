from linebot.models import TextSendMessage, SendMessage


def line_reply_handler(message) -> SendMessage:
    reply_message = repeat(message)
    return reply_message


def repeat(message) -> TextSendMessage:
    reply_message = TextSendMessage(text=message)
    return reply_message

