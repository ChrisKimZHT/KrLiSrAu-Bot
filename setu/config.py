from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_setu_default_size: str = "original"
    klsa_setu_proxy_url: str = ""
    klsa_setu_prefix_url: str = ""
    klsa_setu_withdraw_interval: int = 0
    klsa_setu_cooldown_time: int = 5
    klsa_setu_send_sfw: bool = True
    klsa_setu_send_nsfw: bool = False
    klsa_setu_obfuscate: bool = False


driver = get_driver()
global_config = driver.config
setu_config = Config.parse_obj(global_config.dict())
