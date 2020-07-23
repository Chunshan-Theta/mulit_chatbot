from linebot import LineBotApi
from linebot.models import SendMessage, ImageSendMessage, ImageCarouselColumn, PostbackTemplateAction, \
    TemplateSendMessage, ImageCarouselTemplate, CarouselColumn, CarouselTemplate, MessageAction, URIAction, \
    TextSendMessage


class ImageCarouselElement(dict):
    def __init__(self, url, label):
        super().__init__()
        self.__setitem__("url", url)
        self.__setitem__("label", label)
        self.action = None

    def set_action_postback(self, postback: str, user_send_text=None):
        self.action = PostbackTemplateAction(
            label=self.__getitem__("label"),
            text=user_send_text,
            data=postback
        )
    def set_action_message(self,user_send_text: str):
        self.action = MessageAction(
            label=self.__getitem__("label"),
            text=user_send_text,
        )
    def set_action_url(self,url):
        self.action = URIAction(
            label=self.__getitem__("label"),
            uri=url
        )
class CardCarouselElement(dict):
    def __init__(self, description, title,image_url):
        super().__init__()
        self.__setitem__("description", description)
        self.__setitem__("title", title)
        self.__setitem__("image_url", image_url)
        self.__setitem__("imageBackgroundColor", "#FFFFFF")
        self.actions = list()
        self.default_action = None

    def set_default_action_postback(self,label, postback: str, user_send_text=None):
        self.default_action = PostbackTemplateAction(
            label=label,
            text=user_send_text,
            data=postback
        )
    def set_default_action_message(self,label,user_send_text: str):
        self.default_action = MessageAction(
            label=label,
            text=user_send_text,
        )
    def set_default_action_url(self,label,url):
        self.default_action = URIAction(
            label=label,
            uri=url
        )

    def add_action_postback(self,label, postback: str, user_send_text=None):
        self.actions.append(PostbackTemplateAction(
            label=label,
            text=user_send_text,
            data=postback
        ))

    def add_action_message(self,label,user_send_text: str):
        self.actions.append(MessageAction(
            label=label,
            text=user_send_text,
        ))

    def add_action_url(self,label, url):
        self.actions.append(URIAction(
            label=label,
            uri=url
        ))

class LineBot:
    def __init__(self, Channel_Access_Token):
        self.bot = LineBotApi(Channel_Access_Token)

    #
    def send_message(self,recipient_id:str, message: SendMessage):
        self.bot.push_message(recipient_id, message)

    def send_text_message(self,recipient_id:str, message: str):
        self.send_message(recipient_id, TextSendMessage(message))

    # Picture message
    def send_a_picture(self,recipient_id,original_content_url, preview_image_url):
        message = ImageSendMessage(
            original_content_url=original_content_url,
            preview_image_url=preview_image_url
        )
        self.send_message(recipient_id=recipient_id,message=message)

    def send_carousel_picture(self,recipient_id, default_text, images: [ImageCarouselElement]):
        columns = list()

        for img in images:
            assert img.action is not None, "image action is Not setting"
            tmp_img = ImageCarouselColumn(
                    image_url=img['url'],
                    action=img.action
            )
            columns.append(tmp_img)


        message = TemplateSendMessage(
            alt_text=default_text,
            template=ImageCarouselTemplate(
                columns=columns
            )
        )
        self.send_message(recipient_id=recipient_id, message=message)

    def send_carousel_card(self,recipient_id, default_text, cards: [CardCarouselElement]):
        columns = list()

        for card in cards:
            tmp_img = CarouselColumn(
                 text=card['description'], title=card['title'],
                 thumbnail_image_url=card['image_url'], image_background_color=card['image_background_color'],
                 actions=card.actions, default_action=card.default_action)
            columns.append(tmp_img)


        message = TemplateSendMessage(
            alt_text=default_text,
            template=CarouselTemplate(
                columns=columns
            )
        )
        self.send_message(recipient_id=recipient_id, message=message)

