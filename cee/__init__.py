import datetime
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="高考倒计时",
    description="查询高考倒计时",
    usage="""指令: cee / gk / 高考
用法: cee <年份> - 查询指定年份高考倒计时""",
    extra={
        "authors": "ChrisKim",
        "version": "1.0.1",
        "KrLiSrAu-Bot": True,
    }
)

cee = on_command("cee", aliases={"gk", "高考"}, priority=1, block=True)


@cee.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    now_time = datetime.datetime.now()
    if args.extract_plain_text() == "":  # 如果没给参数
        cee_year = now_time.year
        if (datetime.datetime.strptime(f"{cee_year}-06-07 08:00", "%Y-%m-%d %H:%M") - now_time).total_seconds() <= 0:
            cee_year += 1  # 如果今年高考已过，那么计算明年高考
    else:
        cee_year = args.extract_plain_text()
        if not (cee_year.isdigit() and len(cee_year) == 4 and 1 <= int(cee_year) <= 9999):  # 错误年份
            await cee.finish(MessageSegment.text("年份错误"))

    time_delta = datetime.datetime.strptime(f"{cee_year}-06-07 08:00", "%Y-%m-%d %H:%M") - now_time
    result = f"【高考倒计时】\n" \
             f"距离 {cee_year} 年高考还有：\n" \
             f"{time_delta.days} 天 {time_delta.seconds // 3600} 时 {time_delta.seconds % 3600 // 60} 分 {time_delta.seconds % 60} 秒"
    await cee.finish(MessageSegment.text(result))
