from nonebot import get_driver
from .store_manage import read_data, write_data
from .todo_class import Todo
from typing import Union

driver = get_driver()

data: dict = {}
status: bool = True


@driver.on_startup
async def _load_data() -> None:
    global data
    data = read_data()
    if "error" in data:
        global status
        status = False
    if len(data) == 0:
        data = {
            "private": {},
            "group": {}
        }
        write_data(data)


@driver.on_shutdown
async def _save_data() -> None:
    if status:
        write_data(data)


def _check_init(user_id: Union[int, None] = None, group_id: Union[int, None] = None) -> None:
    if user_id is not None and user_id not in data["private"]:
        data["private"][user_id] = []
    elif group_id is not None and group_id not in data["group"]:
        data["group"][group_id] = []


async def add_private(user_id: int, todo: Todo):
    _check_init(user_id=user_id)
    data["private"][user_id].append(todo)
    await _save_data()


async def add_group(group_id: int, todo: Todo):
    _check_init(group_id=group_id)
    data["group"][group_id].append(todo)
    await _save_data()


async def query_private(user_id: int) -> list:
    _check_init(user_id=user_id)
    return data["private"][user_id]


async def query_group(group_id: int) -> list:
    _check_init(group_id=group_id)
    return data["group"][group_id]
