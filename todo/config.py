from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_todo_schedule: bool = False
    klsa_todo_schedule_hour: str = "9"
    klsa_todo_schedule_minute: str = "0"
    klsa_todo_schedule_group: list = []
    klsa_todo_schedule_user: list = []


driver = get_driver()
global_config = driver.config
todo_config = Config.parse_obj(global_config.dict())
