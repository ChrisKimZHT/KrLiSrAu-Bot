from nonebot import on_command, require, get_bot
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent, MessageEvent, Bot
from .todo_class import Todo
from .todo import *
from .config import todo_config, Config
from typing import Union
import time

__plugin_meta__ = PluginMetadata(
    name="事项",
    description="管理待办事项",
    usage="""指令: todo
用法: todo [选项] <内容>
    空 - 显示帮助
    add - 交互式添加待办
    create <name>;<desc>;<date> - 指令式添加待办
    list [all] - 显示待办事项
    finish <tid> - 标记待办事项为完成
    del <tid> - 删除待办事项
    clear - 清理所有已完成/过期的待办事项""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "1.0.1",
        "KrLiSrAu-Bot": True,
    }
)

todo = on_command("todo", priority=1, block=True)
todo_add = on_command(("todo", "add"), priority=1, block=True)
todo_create = on_command(("todo", "create"), priority=1, block=True)
todo_list = on_command(("todo", "list"), priority=1, block=True)
todo_finish = on_command(("todo", "finish"), priority=1, block=True)
todo_del = on_command(("todo", "del"), priority=1, block=True)
todo_clear = on_command(("todo", "clear"), priority=1, block=True)


@todo.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    await todo.finish(__plugin_meta__.usage)


@todo_add.got("name", prompt="输入事项名称")
@todo_add.got("description", prompt="输入事项描述")
@todo_add.got("timestr", prompt="输入截止时间，格式：YYYY/MM/DD HH:MM")
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], name: str = ArgPlainText(),
            description: str = ArgPlainText(), timestr: str = ArgPlainText()):
    try:
        timestamp = int(time.mktime(time.strptime(timestr, "%Y/%m/%d %H:%M")))
    except Exception as e:
        await todo_add.reject_arg("timestr", "时间格式错误，请重试：\n" + str(e))
        return

    new_todo = Todo(name, description, timestamp)
    if isinstance(event, GroupMessageEvent):
        tid = await add_group(event.group_id, new_todo)
    else:  # isinstance(event, PrivateMessageEvent)
        tid = await add_private(event.user_id, new_todo)
    await todo_add.finish(f"添加成功：{tid}")


@todo_create.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    try:
        [name, discription, date] = args_text.split(";", 2)
        timestamp = int(time.mktime(time.strptime(date, "%Y/%m/%d %H:%M")))
    except Exception as e:
        await todo_create.finish("添加失败：\n" + str(e))
        return
    new_todo = Todo(name, discription, timestamp)
    if isinstance(event, GroupMessageEvent):
        tid = await add_group(event.group_id, new_todo)
    else:  # isinstance(event, PrivateMessageEvent)
        tid = await add_private(event.user_id, new_todo)
    await todo_add.finish(f"添加成功：{tid}")


@todo_list.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    show_all = False
    if args_text == "all":
        show_all = True

    if isinstance(event, GroupMessageEvent):
        data: list = await query_group(event.group_id, show_all)
        message = f"群组 {event.group_id} 的待办事项：\n"
    else:  # isinstance(event, PrivateMessageEvent)
        data: list = await query_private(event.user_id, show_all)
        message = f"用户 {event.user_id} 的待办事项：\n"
    for ele in data:
        message += f"""{"=" * 25}
编号: {ele.get_tid()}{" [已过期]" if ele.is_expired() else ""}{" [已完成]" if ele.is_done() else ""}
时间: {ele.get_timestr()} ({round(abs(ele.get_timedelta()) / 86400, 1)} 天{"前" if ele.is_expired() else "后"})
事项: {ele.get_name()}
描述: {ele.get_description()}
"""
    if len(data) == 0:
        message += "无"
    else:
        message += "=" * 25
    await todo_list.finish(message)


@todo_finish.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    try:
        tid = int(args_text)
    except Exception as e:
        await todo_finish.finish("编号错误：\n" + str(e))
        return

    if isinstance(event, GroupMessageEvent):
        result = await finish_group(event.group_id, tid)
    else:  # isinstance(event, PrivateMessageEvent)
        result = await finish_private(event.user_id, tid)

    if result:
        await todo_finish.finish("操作成功")
    else:
        await todo_finish.finish("操作失败，未找到该编号的事项")


@todo_del.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    try:
        tid = int(args_text)
    except Exception as e:
        await todo_del.finish("编号错误：\n" + str(e))
        return

    if isinstance(event, GroupMessageEvent):
        result = await del_group(event.group_id, tid)
    else:
        result = await del_private(event.user_id, tid)

    if result:
        await todo_del.finish("操作成功")
    else:
        await todo_del.finish("操作失败，未找到该编号的事项")


@todo_clear.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]):
    if isinstance(event, GroupMessageEvent):
        await clear_group(event.group_id)
    else:
        await clear_private(event.user_id)
    await todo_clear.finish("操作成功")


if todo_config.klsa_todo_schedule:
    require("nonebot_plugin_apscheduler")
    from nonebot_plugin_apscheduler import scheduler


    @scheduler.scheduled_job("cron", hour=todo_config.klsa_todo_schedule_hour,
                             minute=todo_config.klsa_todo_schedule_minute, id="todo")
    async def _():
        bot = get_bot()
        for group in todo_config.klsa_todo_schedule_group:
            message = f"【定时发送】群组 {group} 的待办事项：\n"
            data: list = await query_group(int(group))
            if len(data) == 0:
                continue
            for ele in data:
                message += f"""{"=" * 25}
编号: {ele.get_tid()}{" [已过期]" if ele.is_expired() else ""}{" [已完成]" if ele.is_done() else ""}
时间: {ele.get_timestr()} ({round(abs(ele.get_timedelta()) / 86400, 1)} 天{"前" if ele.is_expired() else "后"})
事项: {ele.get_name()}
描述: {ele.get_description()}
"""
            message += "=" * 25
            await bot.call_api("send_group_msg", group_id=group, message=message)
        for user in todo_config.klsa_todo_schedule_user:
            message = f"【定时发送】用户 {user} 的待办事项：\n"
            data: list = await query_private(int(user))
            if len(data) == 0:
                continue
            for ele in data:
                message += f"""{"=" * 25}
编号: {ele.get_tid()}{" [已过期]" if ele.is_expired() else ""}{" [已完成]" if ele.is_done() else ""}
时间: {ele.get_timestr()} ({round(abs(ele.get_timedelta()) / 86400, 1)} 天{"前" if ele.is_expired() else "后"})
事项: {ele.get_name()}
描述: {ele.get_description()}
"""
            message += "=" * 25
            await bot.call_api("send_private_msg", user_id=user, message=message)
