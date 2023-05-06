from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters.onebot.v11.helpers import Cooldown, CooldownIsolateLevel
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from .config import chatgpt_config, Config
from .chat_class import Chat
from .usage_info import get_usage_info
from typing import Optional
import time

__plugin_meta__ = PluginMetadata(
    name="ChatGPT",
    description="基于OpenAI接口的聊天机器人",
    usage="""指令: chatgpt / chat
用法: chatgpt [选项] <内容>
    <内容> - 进行连续对话
    single <内容> - 进行一次性对话
    setting - 清除对话预设
    setting <内容> - 设置对话预设（会立即初始化）
    len - 查看对话长度（一问一答算一次）
    pop [front/back] - 删除最早/最晚的一次对话
    reset - 重置对话
    bill - 查看额度 
    help - 查看帮助""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "2.1.1",
        "KrLiSrAu-Bot": True,
    }
)

chatgpt = on_command("chatgpt", aliases={"chat"}, priority=1, block=True)
chatgpt_single = on_command(("chatgpt", "single"), aliases={("chat", "single")}, priority=1, block=True)
chatgpt_setting = on_command(("chatgpt", "setting"), aliases={("chat", "setting")}, priority=1, block=True)
chatgpt_len = on_command(("chatgpt", "len"), aliases={("chat", "len")}, priority=1, block=True)
chatgpt_pop = on_command(("chatgpt", "pop"), aliases={("chat", "pop")}, priority=1, block=True)
chatgpt_reset = on_command(("chatgpt", "reset"), aliases={("chat", "reset")}, priority=1, block=True)
chatgpt_bill = on_command(("chatgpt", "bill"), aliases={("chat", "bill")}, priority=1, block=True)
chatgpt_help = on_command(("chatgpt", "help"), aliases={("chat", "help")}, priority=1, block=True)

chat_instance = {}
chat_setting = {}


@chatgpt.handle(parameterless=[
    Cooldown(
        cooldown=chatgpt_config.klsa_chat_cooldown,
        prompt="冷却时间中",
        isolate_level=CooldownIsolateLevel.USER
    )
])
async def _(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    if args_text == "":
        await chatgpt.finish(__plugin_meta__.usage)
    if user_id not in chat_instance:
        chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
    chat_inst = chat_instance[user_id]
    await chat(matcher, chat_inst, args_text)


@chatgpt_single.handle(parameterless=[
    Cooldown(
        cooldown=chatgpt_config.klsa_chat_cooldown,
        prompt="冷却时间中",
        isolate_level=CooldownIsolateLevel.USER
    )
])
async def _(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    if args_text == "":
        await chatgpt_single.reject("内容不可为空")
    chat_inst = Chat(user_id)
    await chat(matcher, chat_inst, args_text)


@chatgpt_setting.handle()
async def _(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    if args_text == "":
        chat_setting[user_id] = None
        chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
        await chatgpt_setting.finish("清除设定完成")
    else:
        chat_setting[user_id] = args_text
        chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
        chat_inst = chat_instance[user_id]
        await chat(matcher, chat_inst, None)


@chatgpt_len.handle()
async def _(event: MessageEvent):
    user_id = event.user_id
    if user_id not in chat_instance:
        chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
    chat_inst: Chat = chat_instance[user_id]
    await chatgpt_len.finish(f"当前对话长度为{chat_inst.history_len()}")


@chatgpt_pop.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    if user_id not in chat_instance:
        chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
    chat_inst: Chat = chat_instance[user_id]
    if args_text == "front":
        poped = chat_inst.pop_front()
        if poped:
            await chatgpt_pop.finish(f"已删除最早的一次对话，剩余{chat_inst.history_len()}")
        else:
            await chatgpt_pop.finish("当前没有对话")
    elif args_text == "back":
        poped = chat_inst.pop_back()
        if poped:
            await chatgpt_pop.finish(f"已删除最晚的一次对话，剩余{chat_inst.history_len()}")
        else:
            await chatgpt_pop.finish("当前没有对话")
    else:
        await chatgpt_pop.reject("参数错误，front为最早的一次对话，back为最晚的一次对话")


@chatgpt_reset.handle()
async def _(event: MessageEvent):
    user_id = event.user_id
    chat_instance[user_id] = Chat(user_id, chat_setting.get(user_id))
    await chatgpt_reset.finish("重置对话完成")


@chatgpt_bill.handle()
async def _(event: MessageEvent):
    if chatgpt_config.klsa_bill_session == "":
        await chatgpt_bill.finish("额度查询功能不可用")
    result = await get_usage_info()
    await chatgpt_bill.finish(result)


@chatgpt_help.handle()
async def _(event: MessageEvent):
    await chatgpt_help.finish(__plugin_meta__.usage)


def get_info_str(duration: float, usage: (int, int), poped: bool) -> str:
    info_str = "计算耗时: %.2f sec\n单位数量: %d token(s)" % (duration, usage[0] + usage[1])
    if chatgpt_config.klsa_chat_prompt_token_cost != -1 and chatgpt_config.klsa_chat_completion_token_cost != -1:
        info_str += "\n消费金额: $%.6f" % (chatgpt_config.klsa_chat_prompt_token_cost * usage[
            0] / 1000 + chatgpt_config.klsa_chat_completion_token_cost * usage[1] / 1000)
    if poped:
        info_str += "\n[!] 最早的一次对话被删除"
    return info_str


async def chat(matcher: Matcher, chat_inst: Chat, message: Optional[str]) -> None:
    if chat_inst.get_lock():
        await matcher.reject("上次请求还未完成，请稍后再试或强制刷新会话: chat reset")
    await matcher.send("请求已发送，等待接口响应...")
    start_time = time.time()
    content, usage, poped = await chat_inst.chat(message)
    end_time = time.time()
    duration = end_time - start_time
    info_str = get_info_str(duration, usage, poped)
    result = MessageSegment.text(content) + MessageSegment.text("\n\n") + MessageSegment.text(info_str)
    await matcher.finish(result)
