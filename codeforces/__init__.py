from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
import aiohttp
import time

__plugin_meta__ = PluginMetadata(
    name="Codeforces比赛查询",
    description="查询Codeforces比赛",
    usage="""指令: codeforces / cf
用法: codeforces <数量> - 查询最近的指定数量的比赛""",
    extra={
        "authors": "ChrisKim",
        "version": "1.0.1",
        "KrLiSrAu-Bot": True,
    }
)

codeforces = on_command("codeforces", aliases={"cf"}, priority=1, block=True)


@codeforces.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    arg_str = args.extract_plain_text()
    if len(arg_str) and arg_str.isdigit():
        res_cnt = int(arg_str)
    else:
        res_cnt = 3
    origin_dict = await get_list()
    sorted_list = await sort_list(origin_dict, res_cnt)
    result = "【Codeforces比赛】\n"
    for contest in sorted_list:
        result += f"{contest['name']}\n" \
                  f"Type: {contest['type']}\n" \
                  f"Duration: {contest['durationSeconds'] // 60} (min)\n" \
                  f"Time: {time.strftime('%Y/%m/%d(%a) %H:%M', time.localtime(contest['startTimeSeconds']))}\n" \
                  f"------------------------------\n"
    await codeforces.finish(MessageSegment.text(result))


async def get_list() -> dict:
    api = "https://codeforces.com/api/contest.list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=api) as resp:
            return await resp.json()


async def sort_list(original: dict, count: int) -> list:
    result = []
    for contest in original["result"]:
        if contest["phase"] == "BEFORE":
            result.append(contest)
        else:
            break
    result = sorted(result, key=lambda x: x["startTimeSeconds"])
    while len(result) > count:
        result.pop()
    return result
