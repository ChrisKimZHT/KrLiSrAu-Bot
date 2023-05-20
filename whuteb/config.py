from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_whuteb_account: str = ""
    klsa_whuteb_password: str = ""
    klsa_whuteb_area: str = "mafangshan"
    klsa_whuteb_mafangshan_meterid: str = ""
    klsa_whuteb_mafangshan_factorycode: str = ""
    klsa_whuteb_yujiatou_roomno: str = ""
    klsa_whuteb_yujiatou_factorycode: str = ""
    klsa_whuteb_yujiatou_area: str = ""


driver = get_driver()
global_config = driver.config
whuteb_config = Config.parse_obj(global_config.dict())
