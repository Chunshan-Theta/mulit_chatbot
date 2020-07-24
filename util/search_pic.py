import requests
import random

class pic(dict):

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)
        assert self.__getitem__("title")
        assert self.__getitem__("media")
        assert self.__getitem__("url")


class pic_set_obj:
    def __init__(self, query):
        self.pics=[]
        self.pics.extend(get_pics(query=query))

    def get_a_pic(self,only_pic_url=False) -> pic:
        if only_pic_url:
            return random.choice(self.pics)["media"]
        else:
            return random.choice(self.pics)

    def get_pics(self,count) -> [pic]:
        assert count <=50, "Too many"
        return random.choices(population=self.pics, k=count)


def get_pics(query="台北", count=50) -> [dict]:
    def by_qwant():
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
        pic_sets = list()
        for p in response:
            pic_sets.append(pic(**p))
        return pic_sets

    def by_ig():
        hot_rate = 0.75
        discover_rate = 1-hot_rate
        url = "https://www.instagram.com/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&variables={\"tag_name\":\""+query+"\",\"first\":50}"
        r = requests.get(url)
        response = r.json()
        respond_sets = list()
        for p in response['data']['hashtag']['edge_hashtag_to_media']['edges']:
            p = p["node"]
            url = "https://www.instagram.com/p/"+p["shortcode"]+"/"
            title = p["accessibility_caption"] if 'accessibility_caption' in p and p["accessibility_caption"] is not None else p["edge_media_to_caption"]["edges"][0]["node"]["text"]
            likes_count = p["edge_media_preview_like"]["count"]
            p.update({
                "shortcode":p["shortcode"],
                "title": title,
                "media": p["display_url"],
                "url": url,
                "likes_count": int(likes_count)
            })
            respond_sets.append(pic(**p))

        respond_sets.sort(key=lambda elem: elem["likes_count"],reverse=True)
        return_pics_better = respond_sets[:int(count*hot_rate)] if int(count*hot_rate) < len(respond_sets) else respond_sets
        return_pics_discrover = respond_sets[int(count*hot_rate)+1:]
        random.shuffle(return_pics_discrover)
        return_pics_discrover = return_pics_discrover[:int(count*discover_rate)] if int(count*discover_rate) < len(return_pics_discrover) else return_pics_discrover
        return_pics = return_pics_better+return_pics_discrover
        return return_pics
    return by_ig()


def get_a_pic(query="台北", only_pic_url=False) -> dict:

    a = get_pics(query=query)
    if only_pic_url:
        x = [i["media"] for i in a]
        return random.choice(x)
    else:
        return random.choice(a)

#print(get_pics())