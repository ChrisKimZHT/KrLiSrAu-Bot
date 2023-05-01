from nonebot import require
import pickle

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store


def read_data() -> dict:
    if not store.get_data_file("todo", "data.dat").exists():
        write_data({})
    with open(store.get_data_file("todo", "data.dat"), "rb") as file:
        return pickle.load(file)


def write_data(data: dict) -> None:
    with open(store.get_data_file("todo", "data.dat"), "wb") as file:
        pickle.dump(data, file)
