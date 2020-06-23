from linebot.models import TextSendMessage, SendMessage, ImageSendMessage


def line_reply_handler(message) -> SendMessage:
    if message == "來點圖片":
        return random_photo()
    else:
        return repeat(message)


def repeat(message) -> TextSendMessage:
    reply_message = TextSendMessage(text=message)
    return reply_message


def random_photo() -> TextSendMessage:
    reply_message = ImageSendMessage(
        original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s',
        preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s'
    )
    return reply_message
