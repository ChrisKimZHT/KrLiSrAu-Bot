import asyncio
from nonebot.adapters.onebot.v11 import Bot
from .config import setu_config


async def add_withdraw_job(bot: Bot, message_id: int) -> None:
    if setu_config.klsa_setu_withdraw_interval:
        tasks = [withdraw_msg(bot, message_id)]
        await asyncio.sleep(setu_config.klsa_setu_withdraw_interval)
        await asyncio.gather(*tasks)


async def withdraw_msg(bot: Bot, message_id: int) -> None:
    await bot.delete_msg(message_id=message_id)
