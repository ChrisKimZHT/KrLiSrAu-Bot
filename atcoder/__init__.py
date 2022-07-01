from nonebot import on_command
from .crawler import req_page, get_data

atcoder = on_command("atcoder", aliases={"atc"}, priority=1)


@atcoder.handle()
async def handle_atcoder():
    html = await req_page()
    result = await get_data(html)
    await atcoder.finish(result)
