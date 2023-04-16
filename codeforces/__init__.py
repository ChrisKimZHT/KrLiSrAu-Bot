from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.params import CommandArg
import requests
import time

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
    respounce = requests.get(api)
    return respounce.json()


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
