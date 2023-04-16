from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from .download import req_page
from .resolve import analy_page

atcoder = on_command("atcoder", aliases={"atc"}, priority=1, block=True)


@atcoder.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    # 0-All 1-ABC 2-ARC 3-AGC 4-AHC
    if args.extract_plain_text().lower() == "abc":
        filter_type = 1
    elif args.extract_plain_text().lower() == "arc":
        filter_type = 2
    elif args.extract_plain_text().lower() == "agc":
        filter_type = 3
    elif args.extract_plain_text().lower() == "ahc":
        filter_type = 4
    else:
        filter_type = 0

    html = await req_page()
    contest_list = await analy_page(html)

    result = "【Atcoder比赛】\n" \
             "Start Time    | Name   | Dura.\n"
    for contest in contest_list:
        if filter_type == 0 or contest["type"] == filter_type:
            result += f"{contest['date']} | {contest['name']} | {contest['dura']}\n"

    await atcoder.finish(MessageSegment.text(result))
