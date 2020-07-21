import requests
import random

class pic_set_obj:
    def __init__(self,query):
        self.pics=[]
        self.pics.extend(get_pics(query=query))

    def get_a_pic(self,only_pic_url=False):
        if only_pic_url:
            return random.choice(self.pics)["media"]
        else:
            return random.choice(self.pics)
    def get_pics(self,count):
        assert count <=50, "Too many"
        return random.choices(population=self.pics,k=count)

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
    response = r.json()
    print(f"get_pics:query->{query},re: {response}")
    response = response.get('data').get('result').get('items')
    return response


def get_a_pic(query="台北", only_pic_url=False):

    a = get_pics(query=query)
    if only_pic_url:
        x = [i["media"] for i in a]
        return random.choice(x)
    else:
        return random.choice(a)

#print(get_pics())