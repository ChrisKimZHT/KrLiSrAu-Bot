from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_bot_exec_enable: bool = False


driver = get_driver()
global_config = driver.config
bot_config = Config.parse_obj(global_config.dict())
