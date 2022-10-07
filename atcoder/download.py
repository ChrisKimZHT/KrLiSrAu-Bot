import requests


async def req_page() -> str:
    url = "https://atcoder.jp/contests/"
    headers = {
        "referer": "https://atcoder.jp/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    respounce = requests.get(url, headers=headers)
    return respounce.content.decode("UTF-8")
