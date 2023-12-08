from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from .download import req_page
from .resolve import analy_page
from .parse_problem import parse_problem

__plugin_meta__ = PluginMetadata(
    name="AtCoder比赛查询",
    description="查询AtCoder比赛信息",
    usage="""指令: atcoder / atc
用法: atcoder [选项] <内容>
    空 - 显示指令用法
    list <类型> - 显示对应类型的比赛(abc/arc/agc/ahc)，为空则为全部
    parse <链接> - 将题目解析为Markdown格式""",
    extra={
        "authors": "ChrisKim",
        "version": "1.1.0",
        "KrLiSrAu-Bot": True,
    }
)

atcoder = on_command("atcoder", aliases={"atc"}, priority=1, block=True)
atcoder_list = on_command(("atcoder", "list"), aliases={("atc", "list")}, priority=1, block=True)
atcoder_parse = on_command(("atcoder", "parse"), aliases={("atc", "parse")}, priority=1, block=True)


@atcoder.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    await atcoder.finish(__plugin_meta__.usage)


@atcoder_list.handle()
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

    await atcoder_list.finish(MessageSegment.text(result))


@atcoder_parse.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    url = args.extract_plain_text()
    if not url.startswith("https://atcoder.jp/"):
        await atcoder_parse.finish("链接格式错误")
    result = await parse_problem(url)
    await atcoder_parse.finish(result)
