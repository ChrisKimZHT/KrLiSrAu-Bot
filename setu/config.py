from nonebot import get_driver
from pydantic import BaseModel


class SetuConfig(BaseModel):
    klsa_setu_default_size: str = "original"
    klsa_setu_proxy_url: str = ""
    klsa_setu_prefix_url: str = ""
    klsa_setu_withdraw_interval: int = 0
    klsa_setu_cooldown_time: int = 10


driver = get_driver()
global_config = driver.config
config: SetuConfig = SetuConfig.parse_obj(global_config.dict())
