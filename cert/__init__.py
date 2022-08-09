from datetime import datetime
import subprocess
import re
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

cert = on_command("cert", aliases={"ssl", "证书"}, priority=1)


@cert.handle()
async def handle_cert(args: Message = CommandArg()):
    command = f"curl -Ivs {args} --connect-timeout 10"
    cert_info = subprocess.getstatusoutput(command)[1]
    start_date = datetime.strptime(re.search("start date: (.*)", cert_info).group(1), "%b %d %H:%M:%S %Y GMT")
    expire_date = datetime.strptime(re.search("expire date: (.*)", cert_info).group(1), "%b %d %H:%M:%S %Y GMT")
    message = f"【证书查询】\n" \
              f"域名: {args}\n" \
              f"签发日期: {start_date}\n" \
              f"失效日期: {expire_date}\n" \
              f"剩余时间: {(expire_date - datetime.now()).days}"
    await cert.finish(message)
