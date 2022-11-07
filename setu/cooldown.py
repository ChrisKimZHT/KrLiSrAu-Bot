from time import time
from .config import config

last_respounce = {}


async def check_cd(user_id: int) -> bool:
    if user_id not in last_respounce:
        return True
    time_now = time()
    return last_respounce[user_id] + config.klsa_setu_cooldown_time < time_now


async def update_cd(user_id: int) -> None:
    last_respounce[user_id] = time()
