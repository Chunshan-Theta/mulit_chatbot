import requests
import random


def get_pics(query = "台北",count=50):
    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': count,
            'q': query,
            't': 'images',
            'safesearch': 0,
            'locale': 'en_US',
            'uiv': 1
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )
    #print(r.json())
    response = r.json().get('data').get('result').get('items')
    return response


def get_a_pic(query="台北",only_pic_url=False):

    a = get_pics(query=query)
    if only_pic_url:
        x = [i["media"] for i in a]
        return random.choice(x)
    else:
        return random.choice(a)

#print(get_pics())