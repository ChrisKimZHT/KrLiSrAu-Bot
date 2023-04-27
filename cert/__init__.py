from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.params import CommandArg
import subprocess
import re
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="证书查询",
    description="查询网站SSL证书信息",
    usage="""指令: cert / ssl / 证书
用法: cert <域名> - 查询指定域名的证书信息""",
    extra={
        "authors": "ChrisKim",
        "version": "1.0.1",
        "KrLiSrAu-Bot": True,
    }
)

cert = on_command("cert", aliases={"ssl", "证书"}, priority=1, block=True)


@cert.handle()
async def handle_cert(event: MessageEvent, args: Message = CommandArg()):
    if not re.match(r"https://", str(args)):
        domain = "https://" + str(args)
    else:
        domain = str(args)
    command = f"curl -Ivs {domain} --connect-timeout 3"  # 组合指令
    output = subprocess.getstatusoutput(command)[1]
    result = f"【证书查询】"
    try:
        cert_info = re.search(r"\* Server certificate:\n(\*  .+\n)+", output).group()
        # cert_info = re.sub(r"\* Server certificate:\n", "", cert_info)
        cert_info = re.sub(r"\* +", "", cert_info)  # 去开头的*和空格
        result += "查询成功：\n" + cert_info
    except:
        result += "查询失败！"
    await cert.finish(MessageSegment.text(result))
