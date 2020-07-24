from MongoDbTool.common import MongoBasicClient
from fb_message_bot.fb_attachment import AttachmentGeneric, AttachmentGenericPayloadElements
from fb_message_bot.fb_button import FbButtomPostBack,FbButtomURL
from fb_message_bot.fb_quickreply import FbQuickReply, FbQuickReplyElement
from util.search_pic import get_pics, get_a_pic, pic_set_obj


def handler_pic_search(bot,recipient_id,text):
    query = text[text.index(":")+1:]
    pics = pic_set_obj(query=query)
    url = pics.get_a_pic(only_pic_url=True)
    while url.find("https") == -1:
        url = pics.get_a_pic(only_pic_url=True)

    respond = bot.add_whitelist_website(access_token=bot.access_token, whitelisted_domains=[url])
    print(f"respond:add_whitelist_website: {respond}")
    bot.send_image_url(recipient_id=recipient_id, image_url=url)

def handler_pic_set_search(bot,recipient_id,text):

    query = text[text.index(":")+1:]
    print(f"query: {query}")
    pics_obj = pic_set_obj(query=query)
    pics = pics_obj.get_pics(count=9)

    #
    pic_sets = list()
    whitelisted_domains = list()
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="fbbot_like_pic",
                          db_list_name="pic") as db_client:

        db_client_insert_Elements = list()
        for p in pics:
            while p['url'].find("https") == -1 or p['media'].find("https") == -1:
                p = pics_obj.get_a_pic()

            #
            whitelisted_domains.append(p['url'])
            whitelisted_domains.append(p['media'])

            #
            normal_btn_set = list()
            payload = f"LIKES_PIC:{recipient_id}:{p['shortcode']}"
            normal_btn_set.append(FbButtomPostBack(payload=payload, title="我喜歡這個"))
            normal_btn_set.append(FbButtomURL(url=p['url'], title="前進網站"))

            Element = AttachmentGenericPayloadElements(title=p["title"], subtitle=f"圖片來源:{p['url']}", image_url=p['media'],
                                                        default_url=p['url'], buttons=normal_btn_set,fallback_url=p['media'])
            pic_sets.append(Element)
            db_client_insert_Element = Element.copy()
            db_client_insert_Element.update({
                'shortcode': p['shortcode']
            })
            db_client_insert_Elements.append(db_client_insert_Element)
        db_client.insert_multi(vals=db_client_insert_Elements)

    # reload button
    reload_btn_set = list()
    reload_btn_set.append(FbButtomPostBack(payload=f"搜尋:{query}", title=f"搜尋更多"))

    Element = AttachmentGenericPayloadElements(title="沒有滿意的圖片？", subtitle=f"搜尋更多圖片:{query}", image_url="https://www.catster.com/wp-content/uploads/2018/04/Angry-cat-sound-and-body-language.jpg",
                                               default_url="https://www.catster.com/wp-content/uploads/2018/04/Angry-cat-sound-and-body-language.jpg", buttons=reload_btn_set)
    pic_sets.append(Element)

    pic_sets_AttachmentGeneric = AttachmentGeneric(elements=pic_sets)

    respond = bot.add_whitelist_website(access_token=bot.access_token, whitelisted_domains=whitelisted_domains)
    print(f"respond:add_whitelist_website: {respond}")

    print(f"pic_sets_AttachmentGeneric: {pic_sets_AttachmentGeneric}")
    respond = bot.send_templete_message(recipient_id=recipient_id, message_obj=pic_sets_AttachmentGeneric)
    print(f"respond:bot.send_templete_message: {respond}")


basic_operation_quick_reply_element_search = FbQuickReplyElement(title="搜尋:耶誕城", payload="搜尋",image_url="https://cdn1.iconfinder.com/data/icons/free-98-icons/32/search-256.png")
basic_operation_quick_reply_element_mylikes = FbQuickReplyElement(title="我的最愛", payload="我的最愛",image_url="https://cdn2.iconfinder.com/data/icons/circle-icons-1/64/heart-256.png")

basic_operation_quick_reply = FbQuickReply(text="還想做點什麼嗎？:",elements=[basic_operation_quick_reply_element_search,basic_operation_quick_reply_element_mylikes])
