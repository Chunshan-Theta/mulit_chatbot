
from line_bot.line_helper import LineBot
from line_bot.line_templete import ImageCarouselElement_demo1, CardCarouselElement_domo1

blackman_pic_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s'


def line_reply_handler(bot:LineBot,recipient_id,message:str):
    if message == "來點圖片":
        bot.send_a_picture(recipient_id=recipient_id, original_content_url=blackman_pic_url,preview_image_url=blackman_pic_url)
    elif message == "多點圖片":
        bot.send_carousel_picture(recipient_id=recipient_id,default_text="選一個黑人",images=[ImageCarouselElement_demo1]*3)
    elif message == "選":
        bot.send_carousel_card(recipient_id=recipient_id,default_text="跟一個黑人打招呼",cards=[CardCarouselElement_domo1]*3)
    else:
        bot.send_text_message(recipient_id=recipient_id, message=message)

