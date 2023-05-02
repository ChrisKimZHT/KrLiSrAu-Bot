from nonebot import on_command
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent, MessageEvent, Bot
from .todo_class import Todo
from .todo import *
from typing import Union
import time

__plugin_meta__ = PluginMetadata(
    name="事项",
    description="管理待办事项",
    usage="""指令: todo
用法: """,
    config=None,
    extra={
        "authors": "ChrisKim",
        "version": "1.0.0",
        "KrLiSrAu-Bot": True,
    }
)

todo = on_command("todo", priority=1, block=True)
todo_add = on_command(("todo", "add"), priority=1, block=True)
todo_list = on_command(("todo", "list"), priority=1, block=True)
todo_finish = on_command(("todo", "finish"), priority=1, block=True)
todo_del = on_command(("todo", "del"), priority=1, block=True)
todo_clear = on_command(("todo", "clear"), priority=1, block=True)


@todo.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    pass


@todo_add.got("name", prompt="输入事项名称")
@todo_add.got("description", prompt="输入事项描述")
@todo_add.got("timestr", prompt="输入截止时间，格式：YYYY/MM/DD HH:MM")
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent], name: str = ArgPlainText(),
            description: str = ArgPlainText(), timestr: str = ArgPlainText()):
    try:
        timestamp = int(time.mktime(time.strptime(timestr, "%Y/%m/%d %H:%M")))
    except Exception as e:
        await todo_add.finish("添加失败：\n" + str(e))
        return

    new_todo = Todo(name, description, timestamp)
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
