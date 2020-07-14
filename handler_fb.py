from util.search_pic import get_a_pic


def handler_pic_search(bot,recipient_id,text):
    query = text[text.index(":"):]
    url = get_a_pic(query=query,only_pic_url=True)
    bot.send_image_url(recipient_id=recipient_id, image_url=url)

