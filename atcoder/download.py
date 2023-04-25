import aiohttp


async def req_page() -> str:
    url = "https://atcoder.jp/contests/"
    headers = {
        "referer": "https://atcoder.jp/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            return await resp.text()
