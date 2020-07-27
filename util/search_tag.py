import requests
import random

cookies = "ig_did=84C5F4B7-B10B-43A8-9E97-C003F5489257; mid=XrpVSQAEAAG5mSxPmiLmYjFt-76v; fbm_124024574287414=base_domain=.instagram.com; fbsr_124024574287414=wKu85kOKKzHWYmfATzvwVL20z91yFDDxlMW78MOIXxA.eyJ1c2VyX2lkIjoiMTAwMDAxNjkzODUxMzAzIiwiY29kZSI6IkFRQ0FWQm5NT1ZCeVNzM2F6QjJPMThVanlOY0hYc0R5Rmd2bFIzV2tRX0lOOGl1NDQtWlFQNkFpRnBvMDRkTURic2ZvZ0xFQ01PZF9MT2NRNmRURUU4WFRWalFzQVpQVzRPZDFsNTZvQ2I0Z2JTTVRfNVJ4OXFOYWt6R3pNckxyM2d3R0g1RXY0eHo3UVRTcDZJdkY2SGprOFJwSUE2SjNHMEVlem5tTERoRW5NU3h6NmdCT0duNHY2R3ZxTTJ2MEd0NjlTSGZtTF9GZE1tSlU1ak1yUmtuekFqQ1oxeS0tVFMtNVJfYTBSS1RFWE5RanJXdEhxLTU3U0tXVURYQU05OEJRU1l3ZXNJQmtpdVFBM3FKSTd5MnNBeDBsZUIyblNHVHZQV0JzbkNFZld4WXBNMDRicFU2MEhrNk9FR2hubEpGOEtwSU02d0JVYTNERkQ4UjNDRlJjIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU9pRG9NTFZQcXhsN1B2S3hMdUZZeHhZS2JFaTA4VFg2bmFKcU44N2sxbUdvWkMwaGtzNzNhQVF2SGFYalVjdGZ6bW1nYTUwZmNENlNlRmVZTmpsUE1wVlE1ZTFVOFljaVZoRlUyWGR4bkowN1h5WkI4OWxYeU0ybVVnUFJ0dXdmcHFMcEMyakk1YU5WSURYcHhmWTFlQjAwZmR6NjFKMzBYVUhNcyIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNTk0NzA3MTA3fQ; csrftoken=WVezrHalal5fuAZkyW0e2nPerB7XnuJf; ds_user_id=8760962357; sessionid=8760962357%3Ai6zwow7qC0ClPG%3A4; datr=x1INX5FKHT8-zKs87x4ZSb00; shbid=6763; shbts=1595319606.7683408; rur=PRN; urlgen=\"{\"211.21.120.39\": 3462\054 \"211.22.98.180\": 3462\054 \"59.120.21.25\": 3462}:1jysds:HDvZighsB34zgf4b7PQGKbpgteo\""


def get_tags(query="台北",count=5) -> [str]:

    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query=%23{query}&rank_token=0.18092762642986382&include_reel=true"
    r = requests.get(url,headers={"cookie":cookies})

    return [row["hashtag"]["name"] for row in r.json()["hashtags"]][:count]

