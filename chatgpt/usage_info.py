import aiohttp
from .config import chatgpt_config


async def _request_api() -> dict:
    api = chatgpt_config.klsa_chat_bill_api_url
    headers = {
        "Authorization": "Bearer " + chatgpt_config.klsa_chat_bill_session
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=api, headers=headers) as resp:
            return await resp.json()


async def get_usage_info():
    try:
        resp = await _request_api()
    except Exception as e:
        return f"网络请求错误: {e}"

    result = "总额度: $%.2f\n已使用: $%.2f\n剩余量: $%.2f (%.1f%%)" % (
        resp.get("total_granted"), resp.get("total_used"), resp.get("total_available"),
        resp.get("total_available") / resp.get("total_granted") * 100)
    return result
