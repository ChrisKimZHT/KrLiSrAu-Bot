from nonebot import get_driver
from pydantic import BaseModel


class ChatConfig(BaseModel):
    klsa_chat_api_url: str = "https://api.openai.com/v1/chat/completions"
    klsa_chat_api_key: str = ""
    klsa_chat_model: str = "gpt-3.5-turbo"
    klsa_chat_kt_cost: float = -1


driver = get_driver()
global_config = driver.config
config: ChatConfig = ChatConfig.parse_obj(global_config.dict())
