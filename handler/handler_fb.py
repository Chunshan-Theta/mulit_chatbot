from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack,FbButtomURL
from util.search_pic import get_pics, get_a_pic, pic_set_obj


def handler_pic_search(bot,recipient_id,text):
    query = text[text.index(":")+1:]
    pics = pic_set_obj(query=query)
    url = pics.get_a_pic()
    while url.find("https") == -1:
        url = pics.get_a_pic()
    bot.send_image_url(recipient_id=recipient_id, image_url=url)

def handler_pic_set_search(bot,recipient_id,text):
    query = text[text.index(":")+1:]
    print(f"query: {query}")
    pics_obj = pic_set_obj(query=query)
    pics = pics_obj.get_pics(count=5)

    #
    pic_sets = list()
    whitelisted_domains = list()
    for p in pics:
        while p['url'].find("https") == -1 or p['media'].find("https") == -1:
            p = pics_obj.get_a_pic()

        #
        whitelisted_domains.append(p['url'])
        whitelisted_domains.append(p['media'])

        #
        normal_btn_set = list()
        normal_btn_set.append(FbButtomURL(url=p['url'], title="前進網站"))

        Element = AttachmentGenericPayloadElements(title=p["title"], subtitle=f"圖片來源:{p['url']}", image_url=p['media'],
                                                    default_url=p['media'], buttons=normal_btn_set)
        pic_sets.append(Element)
    pic_sets_AttachmentGeneric = AttachmentGeneric(elements=pic_sets)

    bot.add_whitelist_website(access_token=bot.access_token, whitelisted_domains=whitelisted_domains)

    print(f"pic_sets_AttachmentGeneric: {pic_sets_AttachmentGeneric}")
    bot.send_templete_message(recipient_id=recipient_id, message_obj=pic_sets_AttachmentGeneric)


