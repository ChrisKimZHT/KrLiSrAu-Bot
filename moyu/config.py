from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_moyu_str_1: str = "学习再累，一定不要忘记摸鱼哦！累了困了翘水课，上课多去厕所廊道走走，分是老师的，但命是自己的。"
    klsa_moyu_str_2: str = "学习增加老师负担，摸鱼是给老师减负！最后，祝愿天下所有摸鱼人，都能愉快的度过每一天！"
    klsa_moyu_schedule: bool = False
    klsa_moyu_schedule_hour: str = "9"
    klsa_moyu_schedule_minute: str = "0"
    klsa_moyu_schedule_group: list = []
    klsa_moyu_schedule_user: list = []


driver = get_driver()
global_config = driver.config
moyu_config = Config.parse_obj(global_config.dict())
