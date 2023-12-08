from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from .contest_list import contest_list
from .parse_problem import parse_problem

__plugin_meta__ = PluginMetadata(
    name="Codeforces比赛查询",
    description="查询Codeforces比赛",
    usage="""指令: codeforces / cf
用法: codeforces [选项] <内容>
    空 - 显示指令用法
    list <数量> - 查询最近的指定数量的比赛
    parse <链接> - 将题目解析为Markdown格式""",
    extra={
        "authors": "ChrisKim",
        "version": "1.1.0",
        "KrLiSrAu-Bot": True,
    }
)

codeforces = on_command("codeforces", aliases={"cf"}, priority=1, block=True)
codeforces_list = on_command(("codeforces", "list"), aliases={("cf", "list")}, priority=1, block=True)
codeforces_parse = on_command(("codeforces", "parse"), aliases={("cf", "parse")}, priority=1, block=True)


@codeforces.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    await codeforces.finish(__plugin_meta__.usage)


@codeforces_list.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    arg_str = args.extract_plain_text()
    res_cnt = int(arg_str) if len(arg_str) and arg_str.isdigit() else 3
    result = await contest_list(res_cnt)
    await codeforces_list.finish(MessageSegment.text(result))


@codeforces_parse.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    url = args.extract_plain_text()
    if not url.startswith("https://codeforces.com/"):
        await codeforces_parse.finish("链接格式错误")
    result = await parse_problem(url, "en")
    await codeforces_parse.finish(MessageSegment.text(result))
