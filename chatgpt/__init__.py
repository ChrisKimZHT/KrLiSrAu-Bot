from nonebot import on_command, Bot
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent, MessageSegment, Message
from nonebot.adapters.onebot.v11.helpers import Cooldown, CooldownIsolateLevel
from nonebot.message import handle_event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from .config import chatgpt_config, Config
from .chat_class import ChatInst, ChatUser, ChatResult
from .usage_info import get_usage_info
from .storage_manage import get_chat_user
from typing import Optional, Union
import datetime
import time

__plugin_meta__ = PluginMetadata(
    name="ChatGPT",
    description="基于OpenAI接口的聊天机器人",
    usage="""指令: chatgpt / chat
用法: chatgpt [选项] <内容>
    <内容> - 进行连续对话
    single <内容> - 进行一次性对话
    reset <预设ID> - 使用预设重置对话
    len - 查看对话长度（一问一答算一次）
    pop [front/back] - 删除最早/最晚的一次对话
    preset - 查看预设列表
    preset add <预设内容> - 添加预设
    preset del <预设ID> - 删除预设
    exec <内容> - 使用ChatGPT调用其他机器人功能
    bill - 查看额度 
    help - 查看帮助""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "2.3.1",
        "KrLiSrAu-Bot": True,
    }
)

chatgpt = on_command("chatgpt", aliases={"chat"}, priority=1, block=True)
chatgpt_single = on_command(("chatgpt", "single"), aliases={("chat", "single")}, priority=1, block=True)
chatgpt_len = on_command(("chatgpt", "len"), aliases={("chat", "len")}, priority=1, block=True)
chatgpt_pop = on_command(("chatgpt", "pop"), aliases={("chat", "pop")}, priority=1, block=True)
chatgpt_reset = on_command(("chatgpt", "reset"), aliases={("chat", "reset")}, priority=1, block=True)
chatgpt_bill = on_command(("chatgpt", "bill"), aliases={("chat", "bill")}, priority=1, block=True)
chatgpt_help = on_command(("chatgpt", "help"), aliases={("chat", "help")}, priority=1, block=True)
chatgpt_preset = on_command(("chatgpt", "preset"), aliases={("chat", "preset")}, priority=1, block=True)
chatgpt_preset_add = on_command(("chatgpt", "preset", "add"), aliases={("chat", "preset", "add")},
                                priority=1, block=True)
chatgpt_preset_del = on_command(("chatgpt", "preset", "del"), aliases={("chat", "preset", "del")},
                                priority=1, block=True)
chatgpt_exec = on_command(("chatgpt", "exec"), aliases={("chat", "exec")}, priority=1, block=True)


@chatgpt.handle(parameterless=[
    Cooldown(
        cooldown=chatgpt_config.klsa_chat_cooldown,
        prompt="冷却时间中",
        isolate_level=CooldownIsolateLevel.USER
    )
])
async def _(matcher: Matcher, event: MessageEvent, state: T_State, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    if args_text == "":
        await chatgpt.finish(__plugin_meta__.usage)
    chat_inst: ChatInst = get_chat_user(user_id).get_instance()
    time_now = int(time.time())
    last_use_time = chat_inst.get_last_use_time()
    last_use_timestr = datetime.datetime.fromtimestamp(last_use_time).strftime("%Y-%m-%d %H:%M:%S")
    if time_now - last_use_time > chatgpt_config.klsa_chat_timeout:
        await chatgpt.send(f"该对话上次使用时间为{last_use_timestr}，是否重置？(Y/N)")
        state["user_message"] = args_text
        await chatgpt.skip()
    await chat(matcher, chat_inst, args_text)


@chatgpt.got("is_reset")
async def _(matcher: Matcher, event: MessageEvent, state: T_State, is_reset: Message = ArgPlainText()):
    user_message = state["user_message"]
    user_id = event.user_id
    if is_reset == "Y" or is_reset == "y":
        preset_id = get_chat_user(user_id).get_instance().get_preset_id()
        res: Optional[ChatResult] = await get_chat_user(user_id).reset_instance(preset_id)
        if res is None:
            await chatgpt_reset.finish("无预设重置对话完成")
        else:
            await chatgpt_reset.finish(f"使用预设 {preset_id} 重置对话完成：\n" + res.get_content_str())

    chat_inst: ChatInst = get_chat_user(user_id).get_instance()
    await chat(matcher, chat_inst, user_message)


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
    chat_inst = ChatInst(user_id)
    await chat(matcher, chat_inst, args_text)


@chatgpt_len.handle()
async def _(event: MessageEvent):
    user_id = event.user_id
    chat_inst: ChatInst = get_chat_user(user_id).get_instance()
    await chatgpt_len.finish(f"当前对话长度为{chat_inst.history_len()}")


@chatgpt_pop.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id
    chat_inst: ChatInst = get_chat_user(user_id).get_instance()
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
async def _(event: MessageEvent, args: Message = CommandArg()):
    user_id = event.user_id
    arg_text = args.extract_plain_text()
    try:
        preset_idx = int(arg_text)
    except ValueError:
        preset_idx = -1
    chat_user: ChatUser = get_chat_user(user_id)
    res: Optional[ChatResult] = await chat_user.reset_instance(preset_idx)
    if res is None:
        await chatgpt_reset.finish("无预设重置对话完成")
    else:
        await chatgpt_reset.finish(f"使用预设 {preset_idx} 重置对话完成：\n" + res.get_content_str())


@chatgpt_bill.handle()
async def _(event: MessageEvent):
    if chatgpt_config.klsa_bill_session == "":
        await chatgpt_bill.finish("额度查询功能不可用")
    result = await get_usage_info()
    await chatgpt_bill.finish(result)


@chatgpt_help.handle()
async def _(event: MessageEvent):
    await chatgpt_help.finish(__plugin_meta__.usage)


async def chat(matcher: Matcher, chat_inst: ChatInst, message: Optional[str]) -> None:
    if chat_inst.get_lock():
        await matcher.reject("上次请求还未完成，请稍后再试或强制刷新会话: chat reset")
    await matcher.send("请求已发送，等待接口响应...")
    chat_result = await chat_inst.chat(message)
    if chat_result.get_error():
        result = MessageSegment.text("失败 > ") + \
                 MessageSegment.text(chat_result.get_content_str())
    else:
        result = MessageSegment.text(chat_result.get_content_str()) + \
                 MessageSegment.text("\n\n") + \
                 MessageSegment.text(chat_result.get_info_str())
    await matcher.finish(result)


@chatgpt_preset.handle()
async def _(event: MessageEvent):
    user_id = event.user_id
    chat_user: ChatUser = get_chat_user(user_id)
    preset_list = chat_user.get_presets()
    result = f"预设列表：\n{'=' * 25}\n"
    for i, preset in enumerate(preset_list):
        result += f"{i}: {preset[:20]}{'...' if len(preset) > 20 else ''}\n{'=' * 25}\n"
    await chatgpt_preset.finish(result)


@chatgpt_preset_add.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    user_id = event.user_id
    arg_text = args.extract_plain_text()
    chat_user: ChatUser = get_chat_user(user_id)
    chat_user.add_presets(arg_text)
    await chatgpt_preset_add.finish("添加预设完成")


@chatgpt_preset_del.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    user_id = event.user_id
    arg_text = args.extract_plain_text()
    try:
        preset_idx = int(arg_text)
    except ValueError:
        await chatgpt_preset_del.reject("参数错误，应为数字")
        return
    chat_user: ChatUser = get_chat_user(user_id)
    chat_user.del_presets(preset_idx)
    await chatgpt_preset_del.finish("删除预设完成")


@chatgpt_exec.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if chatgpt_config.klsa_chat_exec_prompt == "":
        await chatgpt_exec.finish("执行功能不可用，请正确配置 klsa_chat_exec_prompt")
    args_text = args.extract_plain_text()
    debug = False
    if args_text.startswith("debug "):
        debug = True
        args_text = args_text[6:]
    await chatgpt_exec.send("请求已发送，等待接口响应...")
    chat_msg = chatgpt_config.klsa_chat_exec_prompt + args_text  # 输入消息
    chat_inst = ChatInst(event.user_id)  # 获取对话实例
    chat_result = await chat_inst.chat(chat_msg)  # 调用对话接口
    chat_resp = chat_result.get_content_str()  # 提取回复消息
    if debug:
        await chatgpt_exec.send("[debug] ChatGPT返回的信息为：\n" + chat_resp)
    if isinstance(event, PrivateMessageEvent):
        new_event = PrivateMessageEvent(time=event.time,
                                        self_id=event.self_id,
                                        post_type=event.post_type,
                                        sub_type=event.sub_type,
                                        user_id=event.user_id,
                                        message_type=event.message_type,
                                        message_id=event.message_id,
                                        message=chat_resp,
                                        raw_message=chat_resp,
                                        font=event.font,
                                        sender=event.sender)
    else:
        new_event = GroupMessageEvent(time=event.time,
                                      self_id=event.self_id,
                                      post_type=event.post_type,
                                      sub_type=event.sub_type,
                                      user_id=event.user_id,
                                      message_type=event.message_type,
                                      message_id=event.message_id,
                                      message=chat_resp,
                                      raw_message=chat_resp,
                                      font=event.font,
                                      sender=event.sender,
                                      group_id=event.group_id)
    await handle_event(bot, new_event)
