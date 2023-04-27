import datetime
from zhdate import ZhDate
from nonebot import on_command
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="摸鱼办",
    description="查询节假日信息",
    usage="""指令: moyu / 摸鱼
用法: moyu - 查询节假日信息""",
    extra={
        "authors": "ChrisKim",
        "version": "1.0.3",
        "KrLiSrAu-Bot": True,
    }
)

moyu = on_command("moyu", aliases={"摸鱼"}, priority=1, block=True)


@moyu.handle()
async def handle_moyu():
    result = await get_result()
    await moyu.finish(result)


async def get_result() -> str:
    # 周末 元旦 春节 清明 劳动 端午 中秋 国庆
    dist = [0, 0, 0, 0, 0, 0, 0, 0]
    today = datetime.date.today()
    time = datetime.datetime.today().time()

    # 计算日期天数
    dist[0] = 5 - today.weekday()
    if dist[0] == -1:
        dist[0] = 0
    # 元旦 1.1
    dist[1] = (datetime.datetime.strptime(
        f"{today.year}-01-01", "%Y-%m-%d").date() - today).days
    if dist[1] < 0:
        dist[1] = (datetime.datetime.strptime(
            f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days
    # 春节 CHN-1.1
    dist[2] = (ZhDate(today.year, 1, 1).to_datetime().date() - today).days
    if dist[2] < 0:
        dist[2] = (ZhDate(today.year + 1, 1,
                          1).to_datetime().date() - today).days
    # 清明 4.5
    dist[3] = (datetime.datetime.strptime(
        f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
    if dist[3] < 0:
        dist[3] = (datetime.datetime.strptime(
            f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days
    # 劳动 5.1
    dist[4] = (datetime.datetime.strptime(
        f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
    if dist[4] < 0:
        dist[4] = (datetime.datetime.strptime(
            f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days
    # 端午 CHN-5.5
    dist[5] = (ZhDate(today.year, 5, 5).to_datetime().date() - today).days
    if dist[5] < 0:
        dist[5] = (ZhDate(today.year + 1, 5,
                          5).to_datetime().date() - today).days
    # 中秋 CHN-8.15
    dist[6] = (ZhDate(today.year, 8, 15).to_datetime().date() - today).days
    if dist[6] < 0:
        dist[6] = (ZhDate(today.year + 1, 8,
                          15).to_datetime().date() - today).days
    # 国庆 10.1
    dist[7] = (datetime.datetime.strptime(
        f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
    if dist[7] < 0:
        dist[7] = (datetime.datetime.strptime(
            f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days

    # 组合列表并排序
    date_list = [
        {"dist": dist[0], "title": "周末"},
        {"dist": dist[1], "title": "元旦"},
        {"dist": dist[2], "title": "春节"},
        {"dist": dist[3], "title": "清明节"},
        {"dist": dist[4], "title": "劳动节"},
        {"dist": dist[5], "title": "端午节"},
        {"dist": dist[6], "title": "中秋节"},
        {"dist": dist[7], "title": "国庆节"}
    ]
    date_list = sorted(date_list, key=lambda x: x["dist"])

    # 星期字典
    week_day_dict = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日"
    }

    # 设置问候语
    if 6 <= time.hour <= 10:
        greet = "上午好"
    elif 11 <= time.hour <= 13:
        greet = "中午好"
    elif 14 <= time.hour <= 18:
        greet = "下午好"
    else:
        greet = "晚上好"

    # 最终文字组合
    text = f"【摸鱼办】{today.day} 日{greet}！今天是{week_day_dict[today.weekday()]}。\n" \
           f"学习再累，一定不要忘记摸鱼哦！累了困了翘水课，上课多去厕所廊道走走，分是老师的，但命是自己的。\n\n"
    for i in range(0, 7):
        if date_list[i]["dist"] == 0:
            text = text + f"★ 今天就是{date_list[i]['title']}！\n"
        else:
            text = text + \
                   f"☆ 距离{date_list[i]['title']}还有：{date_list[i]['dist']} 天\n"
    text = text + f"\n学习增加老师负担，摸鱼是给老师减负！最后，祝愿天下所有摸鱼人，都能愉快的度过每一天！"
    return text
