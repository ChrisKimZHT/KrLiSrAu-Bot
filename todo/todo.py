from nonebot import get_driver
from .store_manage import read_data, write_data
from .todo_class import Todo
from typing import Union

driver = get_driver()

data: dict = {}
status: bool = False


@driver.on_startup
async def _load_data() -> None:
    global data, status
    data = read_data()
    if len(data) == 0:
        data = {
            "private": {},
            "group": {},
            "tid": 0,
        }
        write_data(data)
    status = True


@driver.on_shutdown
async def _save_data() -> None:
    if status:
        write_data(data)


def _check_init(user_id: Union[int, None] = None, group_id: Union[int, None] = None) -> None:
    if user_id is not None and user_id not in data["private"]:
        data["private"][user_id] = []
    elif group_id is not None and group_id not in data["group"]:
        data["group"][group_id] = []


def _acquire_tid() -> int:
    tid = data["tid"]
    data["tid"] += 1
    return tid


async def add_private(user_id: int, todo: Todo) -> int:
    _check_init(user_id=user_id)
    todo.set_tid(_acquire_tid())
    data["private"][user_id].append(todo)
    await _save_data()
    return todo.get_tid()


async def add_group(group_id: int, todo: Todo) -> int:
    _check_init(group_id=group_id)
    todo.set_tid(_acquire_tid())
    data["group"][group_id].append(todo)
    await _save_data()
    return todo.get_tid()


async def query_private(user_id: int, show_all: bool = False) -> list:
    _check_init(user_id=user_id)
    todo_data = data["private"][user_id]
    todo_data.sort(key=lambda x: x.timestamp)
    if not show_all:
        todo_data = list(filter(lambda x: not x.is_expired(), todo_data))
    return todo_data


async def query_group(group_id: int, show_all: bool = False) -> list:
    _check_init(group_id=group_id)
    todo_data = data["group"][group_id]
    todo_data.sort(key=lambda x: x.timestamp)
    if not show_all:
        todo_data = list(filter(lambda x: not x.is_expired(), todo_data))
    return todo_data
