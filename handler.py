from linebot.models import TextSendMessage, SendMessage, ImageSendMessage, VideoSendMessage, ImagemapSendMessage, \
    BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea


def line_reply_handler(message) -> SendMessage:
    if message == "來點圖片":
        return blackman_questions_photo()
    elif message == "多點圖片":
        return more_lackman_questions_photo()
    else:
        return repeat(message)


def repeat(message) -> TextSendMessage:
    reply_message = TextSendMessage(text=message)
    return reply_message


def blackman_questions_photo() -> ImageSendMessage:
    return ImageSendMessage(
        original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s',
        preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s'
    )


def video() -> VideoSendMessage:
    return VideoSendMessage(
        original_content_url='https://example.com/original.mp4',
        preview_image_url='https://example.com/preview.jpg'
    )


def more_lackman_questions_photo() -> ImagemapSendMessage:
    connect_2_website = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s'
    preview_text = 'this is an imagemap'
    return ImagemapSendMessage(
        base_url=connect_2_website,
        alt_text=preview_text,
        base_size=BaseSize(height=1040, width=1040),
        actions=[
            URIImagemapAction(
                link_uri='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s',
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
                link_uri='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s',
                area=ImagemapArea(
                    x=0, y=520, width=520, height=520
                )
            ),
            URIImagemapAction(
                link_uri='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s',
                area=ImagemapArea(
                    x=520, y=520, width=520, height=520
                )
            )
        ]
    )