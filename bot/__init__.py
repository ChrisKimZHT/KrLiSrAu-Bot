import nonebot
from nonebot import on_command, permission
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, Plugin
from .config import bot_config, Config
import subprocess

__plugin_meta__ = PluginMetadata(
    name="KrLiSrAu-Bot管理",
    description="机器人管理组件",
    usage="""指令: bot
用法: bot [选项]
    空 - 显示指令用法
    plugins - 显示所有插件
    help <插件名> - 显示指定插件用法
    exec <语句> - *管理员* 执行shell语句""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "1.0.0",
        "KrLiSrAu-Bot": True,
    }
)

bot_ = on_command("bot", priority=1, block=True)
bot_plugins = on_command(("bot", "plugins"), priority=1, block=True)
bot_help = on_command(("bot", "help"), priority=1, block=True)
bot_exec = on_command(("bot", "exec"), priority=1, block=True, permission=nonebot.permission.SUPERUSER)


@bot_.handle()
async def _(event: MessageEvent):
    await bot_help.finish(__plugin_meta__.usage)


@bot_plugins.handle()
async def _(event: MessageEvent):
    plugins: set[Plugin] = nonebot.get_loaded_plugins()
    result_chriskim = ""
    result_other = ""

    for plugin in plugins:
        if plugin.metadata.extra.get("KrLiSrAu-Bot") is True:
            result_chriskim += f"v{plugin.metadata.extra.get('version')} - {plugin.name}\n"
        else:
            result_other += f"{plugin.name}\n"

    result = "【插件列表】\n> ChrisKim插件：\n" + result_chriskim + "\n> 其他插件：\n"
    if len(result_other) == 0:
        result += "无"
    else:
        result += result_other

    await bot_plugins.finish(result)


@bot_help.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_test = args.extract_plain_text()
    plugins: set[Plugin] = nonebot.get_loaded_plugins()

    if args_test == "":
        await bot_help.finish(__plugin_meta__.usage)

    for plugin in plugins:
        if plugin.name == args_test:
            help_text = f"""{plugin.metadata.name} - {plugin.metadata.description}
版本: v{plugin.metadata.extra.get("version")}
{plugin.metadata.usage}"""
            await bot_help.finish(help_text)
    else:
        text = """没有查询到此插件，可能原因：
1. 插件名拼写错误，请使用bot plugins查看正确的插件名
2. 该插件非ChrisKim插件，该指令仅支持查询ChrisKim插件"""
        await bot_help.finish(text)


@bot_exec.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if not bot_config.klsa_bot_exec_enable:
        await bot_exec.finish("此功能已被禁用")

    args_test = args.extract_plain_text()

    if args_test == "":
        await bot_exec.finish("请输入要执行的语句")

    resp = subprocess.getoutput(args_test)
    await bot_exec.finish(f"执行结果：\n{resp}")
