import datetime
from nonebot import on_command

cee = on_command("cee", aliases={"gk", "高考"}, priority=1)


@cee.handle()
async def handle_cee():
    now = datetime.datetime.now()
    year = now.year
    if (datetime.datetime.strptime(f"{year}-06-07 08:00", "%Y-%m-%d %H:%M") - now).seconds <= 0:
        year += 1  # 如果今年高考已过，那么计算明年高考
    cee_time = f"{year}-06-07 08:00"
    delta = datetime.datetime.strptime(cee_time, "%Y-%m-%d %H:%M") - now
    result = f"【高考倒计时】\n" \
             f"距离{year}高考还有：\n" \
             f"{delta.days}天{delta.seconds // 3600}小时{delta.seconds % 3600 // 60}分钟{delta.seconds % 60}秒"
    await cee.finish(result)
