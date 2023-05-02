from nonebot import on_command
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent, MessageEvent, Bot
from .todo_class import Todo
from .todo import add_private, add_group, query_private, query_group
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
        await add_group(event.group_id, new_todo)
    else:  # isinstance(event, PrivateMessageEvent)
        await add_private(event.user_id, new_todo)
    await todo_add.finish("添加成功")


@todo_list.handle()
async def _(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]):
    if isinstance(event, GroupMessageEvent):
        data: list = await query_group(event.group_id)
        message = f"群组 {event.group_id} 的待办事项：\n"
    else:  # isinstance(event, PrivateMessageEvent)
        data: list = await query_private(event.user_id)
        message = f"用户 {event.user_id} 的待办事项：\n"
    for ele in data:
        message += f"""{"-" * 25}
{ele.get_timestr()}
{ele.get_name()}
{ele.get_description()}
"""
    if len(data) == 0:
        message += "无"
    else:
        message += "-" * 25
    await todo_list.finish(message)
