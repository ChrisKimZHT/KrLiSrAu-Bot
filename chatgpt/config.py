from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    klsa_chat_api_url: str = "https://api.openai.com/v1/chat/completions"
    klsa_chat_api_key: str = ""
    klsa_chat_cooldown: int = 0
    klsa_chat_model: str = "gpt-3.5-turbo"
    klsa_chat_token_limit: int = 1024
    klsa_chat_timeout: int = 600
    klsa_chat_prompt_token_cost: float = -1
    klsa_chat_completion_token_cost: float = -1
    klsa_chat_bill_api_url: str = "https://api.openai.com/dashboard/billing/credit_grants"
    klsa_chat_bill_session: str = ""
    klsa_chat_exec_prompt: str = ""


driver = get_driver()
global_config = driver.config
chatgpt_config = Config.parse_obj(global_config.dict())
