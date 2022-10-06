import datetime
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg

cee = on_command("cee", aliases={"gk", "高考"}, priority=1)


@cee.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    now = datetime.datetime.now()
    if args.extract_plain_text() == "":  # 如果没给参数
        year = now.year
        if (datetime.datetime.strptime(f"{year}-06-07 08:00", "%Y-%m-%d %H:%M") - now).total_seconds() <= 0:
            year += 1  # 如果今年高考已过，那么计算明年高考
    else:
        year = args.extract_plain_text()
        if not (year.isdigit() and len(year) == 4 and 1 <= int(year) <= 9999):  # 错误年份
            await cee.finish(MessageSegment.text("年份错误"))

    cee_time = f"{year}-06-07 08:00"
    delta = datetime.datetime.strptime(cee_time, "%Y-%m-%d %H:%M") - now
    result = f"【高考倒计时】\n" \
             f"距离 {year} 年高考还有：\n" \
             f"{delta.days} 天 {delta.seconds // 3600} 时 {delta.seconds % 3600 // 60} 分 {delta.seconds % 60} 秒"
    await cee.finish(MessageSegment.text(result))
