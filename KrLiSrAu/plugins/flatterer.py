import random
from nonebot import on_command, CommandSession

with open("./resource/flatter/flatter_text.txt", encoding="UTF-8") as file:
    text = file.read().splitlines()


@on_command("flatter", aliases=("tg", "舔狗"))
async def flatter(session: CommandSession):
    line = random.randint(0, len(text) - 1)
    result = "【舔狗日记】\n" + text[line]
    await session.send(result)
