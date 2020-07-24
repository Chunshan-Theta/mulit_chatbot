from linebot import LineBotApi
from linebot.models import SendMessage, ImageSendMessage, ImageCarouselColumn, PostbackTemplateAction, \
    TemplateSendMessage, ImageCarouselTemplate, CarouselColumn, CarouselTemplate, MessageAction, URIAction, \
    TextSendMessage
import requests


class ImageCarouselElement(dict):
    def __init__(self, url, label):
        super().__init__()
        self.__setitem__("url", url)
        self.__setitem__("label", label)
        self.action = None
        self.action_json = None

    def set_action_postback(self, postback: str, user_send_text=None):
        self.action = PostbackTemplateAction(
            label=self.__getitem__("label"),
            text=user_send_text,
            data=postback
        )
        self.action_json = {
            "type": "postback",
            "label": user_send_text,
            "data": postback
        }

    def set_action_message(self,user_send_text: str):
        self.action = MessageAction(
            label=self.__getitem__("label"),
            text=user_send_text,
        )
        self.action_json = {
            "type": "message",
            "label": self.__getitem__("label"),
            "text": user_send_text
        }

    def set_action_url(self,url):
        self.action = URIAction(
            label=self.__getitem__("label"),
            uri=url
        )
        self.action_json = {
            "type": "uri",
            "label": self.__getitem__("label"),
            "uri": url
        }


class CardCarouselElement(dict):
    def __init__(self, description, title,image_url):
        super().__init__()
        self.__setitem__("description", description)
        self.__setitem__("title", title)
        self.__setitem__("image_url", image_url)
        self.__setitem__("image_background_color", "#FFFFFF")
        self.actions, self.actions_json = list(), list()
        self.default_action, self.default_action_json = None, None

    def set_default_action_postback(self,label, postback: str, user_send_text=None):
        self.default_action = PostbackTemplateAction(
            label=label,
            text=user_send_text,
            data=postback
        )

        self.default_action_json = {
            "type": "postback",
            "label": user_send_text,
            "data": postback
        }

    def set_default_action_message(self,label,user_send_text: str):
        self.default_action = MessageAction(
            label=label,
            text=user_send_text,
        )

        self.default_action_json = {
            "type": "message",
            "label": label,
            "text": user_send_text
        }

    def set_default_action_url(self,label,url):
        self.default_action = URIAction(
            label=label,
            uri=url
        )
        self.default_action_json = {
            "type": "uri",
            "label": label,
            "uri": url
        }

    def add_action_postback(self,label, postback: str, user_send_text=None):
        self.actions.append(PostbackTemplateAction(
            label=label,
            text=user_send_text,
            data=postback
        ))
        self.actions_json.append({
            "type": "postback",
            "label": label,
            "data": postback,
            "text": user_send_text
        })

    def add_action_message(self, label, user_send_text: str):
        self.actions.append(MessageAction(
            label=label,
            text=user_send_text,
        ))
        self.actions_json.append({
            "type": "message",
            "label": label,
            "text": user_send_text
        })

    def add_action_url(self, label, url):
        self.actions.append(URIAction(
            label=label,
            uri=url
        ))
        self.actions_json.append({
            "type": "uri",
            "label": label,
            "uri": url
        })


class LineBot:
    def __init__(self, Channel_Access_Token):
        self.bot = LineBotApi(Channel_Access_Token)
        self.Channel_Access_Token = Channel_Access_Token
        self.push_api_url = "https://api.line.me/v2/bot/message/push"
        self.auth_header = {"Authorization": "Bearer T7WVBSLT4LoxIAvPQV4fQA2cJBq9OxjgLmPiOquiw6e3m8zMKHq83nuXcQ0OXaj5Z/oqni0NgPvX7r9M2MK3rhxi8ZjzTnerMywBxU7/So6AUq3YlJxQmjJd6hWBQ92avWSBLgukv3h9zxziV5wtwwdB04t89/1O/w1cDnyilFU="}
        self.header = {"Content-Type": "application/json"}

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

    ##
    def _push_message(self,recipient_id,messages:[dict]):
        body = {
            "to": recipient_id,
            "messages": messages
        }
        headers = self.header.copy()
        headers.update(self.auth_header)
        re = requests.post(url=self.push_api_url,json=body, headers=headers)
        print(re,re.json())

    def _push_text_message(self,recipient_id,messages:[str]):
        payload_messages = list()
        for m in messages:
            payload_messages.append({
                "type": "text",
                "text": m
            })
        self._push_message(recipient_id=recipient_id,messages=payload_messages)

    # Picture message
    def _push_a_picture(self,recipient_id,original_content_url, preview_image_url):
        message = {
            "type": "image",
            "originalContentUrl": original_content_url,
            "previewImageUrl": preview_image_url
        }
        self._push_message(recipient_id=recipient_id, messages=[message])

    def _push_carousel_picture(self,recipient_id, default_text, images: [ImageCarouselElement]):

        def _make_columns(url, action):
            return {
                        "imageUrl": url,
                        "action": action
                    }
        columns = list()

        for img in images:
            assert img.action_json is not None, "image action is Not setting"
            columns.append(_make_columns(url=img['url'], action=img.action_json))

        messages = [
            {
                "type": "template",
                "altText": default_text,
                "template": {
                    "type": "image_carousel",
                    "columns": columns

                }
            }
        ]
        self._push_message(recipient_id=recipient_id, messages=messages)

    def _push_carousel_card(self,recipient_id, default_text, cards: [CardCarouselElement]):
        def _make_columns(text, title,thumbnail_image_url, image_background_color,actions, default_action):
            return {
                        "thumbnailImageUrl": thumbnail_image_url,
                        "imageBackgroundColor": image_background_color,
                        "title": title,
                        "text": text,
                        "defaultAction": default_action,
                        "actions": actions
                    }
        columns = list()

        for card in cards:

            columns.append(_make_columns(
                text=card['description'],
                title=card['title'],
                thumbnail_image_url=card['image_url'],
                image_background_color=card['image_background_color'],
                actions=card.actions_json,
                default_action=card.default_action_json)
            )

        messages = [
            {
                "type": "template",
                "altText": default_text,
                "template": {
                    "type": "carousel",
                    "columns": columns,
                    "imageAspectRatio": "rectangle",
                    "imageSize": "cover"
                }
            }
        ]
        self._push_message(recipient_id=recipient_id, messages=messages)
