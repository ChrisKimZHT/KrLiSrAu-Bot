from nonebot import get_driver
from .store_manage import read_data, write_data
from .todo_class import Todo
from typing import Union

_driver = get_driver()

_data: dict = {}
_status: bool = False


@_driver.on_startup
async def _load_data() -> None:
    global _data, _status
    _data = read_data()
    if len(_data) == 0:
        _data = {
            "private": {},
            "group": {},
            "tid": 0,
        }
        write_data(_data)
    _status = True


@_driver.on_shutdown
async def _save_data() -> None:
    if _status:
        write_data(_data)


def _check_init(user_id: Union[int, None] = None, group_id: Union[int, None] = None) -> None:
    if user_id is not None and user_id not in _data["private"]:
        _data["private"][user_id] = []
    elif group_id is not None and group_id not in _data["group"]:
        _data["group"][group_id] = []


def _acquire_tid() -> int:
    tid = _data["tid"]
    _data["tid"] += 1
    return tid


async def add_private(user_id: int, todo: Todo) -> int:
    _check_init(user_id=user_id)
    todo.set_tid(_acquire_tid())
    _data["private"][user_id].append(todo)
    await _save_data()
    return todo.get_tid()


async def add_group(group_id: int, todo: Todo) -> int:
    _check_init(group_id=group_id)
    todo.set_tid(_acquire_tid())
    _data["group"][group_id].append(todo)
    await _save_data()
    return todo.get_tid()


async def query_private(user_id: int, show_all: bool = False) -> list:
    _check_init(user_id=user_id)
    todo_data = _data["private"][user_id]
    todo_data.sort(key=lambda x: x.timestamp)
    if not show_all:
        todo_data = list(filter(lambda x: (not x.is_expired()) and (not x.is_done()), todo_data))
    return todo_data


async def query_group(group_id: int, show_all: bool = False) -> list:
    _check_init(group_id=group_id)
    todo_data = _data["group"][group_id]
    todo_data.sort(key=lambda x: x.timestamp)
    if not show_all:
        todo_data = list(filter(lambda x: (not x.is_expired()) and (not x.is_done()), todo_data))
    return todo_data


async def finish_private(user_id: int, tid: int) -> bool:
    _check_init(user_id=user_id)
    todo_data = _data["private"][user_id]
    for todo in todo_data:
        if todo.get_tid() == tid:
            todo.set_done()
            await _save_data()
            return True
    return False


async def finish_group(group_id: int, tid: int) -> bool:
    _check_init(group_id=group_id)
    todo_data = _data["group"][group_id]
    for todo in todo_data:
        if todo.get_tid() == tid:
            todo.set_done()
            await _save_data()
            return True
    return False


async def del_private(user_id: int, tid: int) -> bool:
    _check_init(user_id=user_id)
    todo_data = _data["private"][user_id]
    for todo in todo_data:
        if todo.get_tid() == tid:
            todo_data.remove(todo)
            await _save_data()
            return True
    return False


async def del_group(group_id: int, tid: int) -> bool:
    _check_init(group_id=group_id)
    todo_data = _data["group"][group_id]
    for todo in todo_data:
        if todo.get_tid() == tid:
            todo_data.remove(todo)
            await _save_data()
            return True
    return False


async def clear_private(user_id: int) -> None:
    _check_init(user_id=user_id)
    todo_data = _data["private"][user_id]
    _data["private"][user_id] = list(filter(lambda x: (not x.is_expired()) and (not x.is_done()), todo_data))
    await _save_data()


async def clear_group(group_id: int) -> None:
    _check_init(group_id=group_id)
    todo_data = _data["group"][group_id]
    _data["group"][group_id] = list(filter(lambda x: (not x.is_expired()) and (not x.is_done()), todo_data))
    await _save_data()
