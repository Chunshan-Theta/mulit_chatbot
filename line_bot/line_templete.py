from linebot import LineBotApi
from linebot.models import SendMessage, ImageSendMessage, ImageCarouselColumn, PostbackTemplateAction, \
    TemplateSendMessage, ImageCarouselTemplate, CarouselColumn, CarouselTemplate, MessageAction, URIAction

from line_bot.line_helper import ImageCarouselElement, CardCarouselElement

black_man_pic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdNlz5PjZDea1C5tI8p_Tx_mEs84KgCKrM_rJJVXdV9ZooNvo_KA&s"

###
ImageCarouselElement_demo1 = ImageCarouselElement(
    url=black_man_pic,
    label="黑人問號")
ImageCarouselElement_demo1.set_action_message(user_send_text="黑人表示：???")



###
CardCarouselElement_domo1 = CardCarouselElement(description="問號耶",title="黑人",image_url=black_man_pic)
CardCarouselElement_domo1.set_default_action_message(label="go for view",user_send_text="hi 黑人！")
CardCarouselElement_domo1.add_action_message(label="問候他",user_send_text="Hello!")
CardCarouselElement_domo1.add_action_postback(label="偷偷問候他",postback="你已經偷偷問候他了")
CardCarouselElement_domo1.add_action_url(label="去他家看看", url=black_man_pic)



