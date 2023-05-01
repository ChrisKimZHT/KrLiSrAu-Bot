from nonebot import require
import pickle

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store


def read_data() -> dict:
    try:
        if not store.get_data_file("todo", "data.dat").exists():
            write_data({})
        with open(store.get_data_file("todo", "data.dat"), "rb") as file:
            return pickle.load(file)
    except Exception as e:
        return {"error": str(e)}


def write_data(data: dict) -> bool:
    try:
        with open(store.get_data_file("todo", "data.dat"), "wb") as file:
            pickle.dump(data, file)
        return True
    except Exception:
        return False
