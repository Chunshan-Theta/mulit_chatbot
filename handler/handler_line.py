from linebot import LineBotApi
from linebot.models import TextSendMessage, SendMessage, ImageSendMessage, VideoSendMessage, ImagemapSendMessage, \
    BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea, TemplateSendMessage, ImageCarouselTemplate, \
    ImageCarouselColumn, PostbackTemplateAction, ButtonsTemplate, MessageTemplateAction, URITemplateAction, \
    CarouselColumn, CarouselTemplate

from line_bot.line_helper import LineBot
from line_bot.line_templete import ImageCarouselElement_demo1, CardCarouselElement_domo1

blackman_pic_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s'

def line_reply_handler(bot:LineBot,recipient_id,message:str) -> SendMessage:
    if message == "來點圖片":
        bot.send_a_picture(recipient_id=recipient_id, original_content_url=blackman_pic_url,preview_image_url=blackman_pic_url)
    elif message == "多點圖片":
        bot.send_carousel_picture(recipient_id=recipient_id,default_text="選一個黑人",images=[ImageCarouselElement_demo1]*3)
    elif message == "選":
        bot.send_carousel_card(recipient_id=recipient_id,default_text="跟一個黑人打招呼",cards=[CardCarouselElement_domo1]*3)
    else:
        bot.send_text_message(recipient_id=recipient_id, message=message)


# Text message
def repeat(message) -> TextSendMessage:
    reply_message = TextSendMessage(text=message)
    return reply_message


# Picture message
def send_a_picture(original_content_url=blackman_pic_url, preview_image_url=blackman_pic_url) -> ImageSendMessage:
    return ImageSendMessage(
        original_content_url=original_content_url,
        preview_image_url=preview_image_url
    )

"""
def video() -> VideoSendMessage:
    return VideoSendMessage(
        original_content_url='https://example.com/original.mp4',
        preview_image_url='https://example.com/preview.jpg'
    )
"""


# Picture map
# 單張圖，動態點擊區域
# a single pic and multi-clicked area
def map_image() -> ImagemapSendMessage:
    main_photo = blackman_pic_url
    preview_text = 'this is an imagemap'
    return ImagemapSendMessage(
        base_url=main_photo,
        alt_text=preview_text,
        base_size=BaseSize(height=1040, width=1040),
        actions=[
            URIImagemapAction(
                link_uri=blackman_pic_url,
                area=ImagemapArea(
                    x=0, y=0, width=520, height=520
                )
            ),
            MessageImagemapAction(
                text='hello',
                area=ImagemapArea(
                    x=520, y=0, width=520, height=520
                )
            ),
            URIImagemapAction(
                link_uri=blackman_pic_url,
                area=ImagemapArea(
                    x=0, y=520, width=520, height=520
                )
            ),
            URIImagemapAction(
                link_uri=blackman_pic_url,
                area=ImagemapArea(
                    x=520, y=520, width=520, height=520
                )
            )
        ]
    )


def choice_with_a_pictures(title='Menu',text='Please select'):
    return TemplateSendMessage(
    alt_text='we need your choice. please make your choice on you mobile',
    template=ButtonsTemplate(
        thumbnail_image_url=blackman_pic_url,
        title=title,
        text=text,
        actions=[
            PostbackTemplateAction(
                label='postback',
                text=None,
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='output something',
                text='message text'
            ),
            URITemplateAction(
                label='got to site',
                uri=blackman_pic_url
            )
        ]
    )
)

def more_blackman_questions_photo() -> TemplateSendMessage:
    return TemplateSendMessage(
    alt_text='blackman_pic_url',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url=blackman_pic_url,
                action=PostbackTemplateAction(
                    label='postback1',
                    text='postback text1',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url=blackman_pic_url,
                action=PostbackTemplateAction(
                    label='postback2',
                    text='postback text2',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)
