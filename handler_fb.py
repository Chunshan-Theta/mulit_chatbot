from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack,FbButtomURL
from util.search_pic import get_pics,get_a_pic


def handler_pic_search(bot,recipient_id,text):
    query = text[text.index(":"):]
    url = get_a_pic(query=query,only_pic_url=True)
    bot.send_image_url(recipient_id=recipient_id, image_url=url)


def handler_pic_set_search(bot,recipient_id,text):
    query = text[text.index(":"):]
    pics = get_pics(query=query, count=5)
    print(f"pics: {pics}")
    pic_sets = list()
    for p in pics:
        normal_btn_set = list()
        normal_btn_set.append(FbButtomURL(url=p['url'], title="前進網站"))

        Element = AttachmentGenericPayloadElements(title=p["title"], subtitle=f"圖片來源:{p['url']}", image_url=p['media'],
                                                    default_url=p['media'], buttons=normal_btn_set)
        pic_sets.append(Element)
    pic_sets_AttachmentGeneric = AttachmentGeneric(elements=pic_sets)
    print(f"pic_sets_AttachmentGeneric: {pic_sets_AttachmentGeneric}")
    bot.send_templete_message(recipient_id=recipient_id, message_obj=pic_sets_AttachmentGeneric)


