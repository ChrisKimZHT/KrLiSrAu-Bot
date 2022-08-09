from datetime import datetime
import subprocess
import re
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

cert = on_command("cert", aliases={"ssl", "证书"}, priority=1)


@cert.handle()
async def handle_cert(args: Message = CommandArg()):
    if not re.match(r"https://", str(args)):
        domain = "https://" + str(args)
    else:
        domain = str(args)
    command = f"curl -Ivs {domain} --connect-timeout 10"
    cert_info = subprocess.getstatusoutput(command)[1]
    subject = re.search("subject: (.*)", cert_info).group(1)
    start_date = datetime.strptime(re.search("start date: (.*)", cert_info).group(1), "%b %d %H:%M:%S %Y GMT")
    expire_date = datetime.strptime(re.search("expire date: (.*)", cert_info).group(1), "%b %d %H:%M:%S %Y GMT")
    issuer = re.search("issuer: (.*)", cert_info).group(1)
    message = f"[SSL Cert Info]\n" \
              f"Subject: {subject}\n" \
              f"Start date: {start_date}\n" \
              f"Expire date: {expire_date}\n" \
              f"Remain: {(expire_date - datetime.now()).days} Day(s)\n" \
              f"Issuer: {issuer}"
    await cert.finish(message)
