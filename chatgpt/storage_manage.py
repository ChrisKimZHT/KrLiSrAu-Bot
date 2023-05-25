from .chat_class import ChatUser
from nonebot import require, get_driver
import pickle

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_localstore")

from nonebot_plugin_apscheduler import scheduler
import nonebot_plugin_localstore as store

driver = get_driver()
chat_user = {}
version = "v1"


def get_chat_user(user_id: int) -> ChatUser:
    if user_id not in chat_user:
        chat_user[user_id] = ChatUser(user_id)
    return chat_user[user_id]


@driver.on_startup
def load_data():
    global chat_user
    chat_user = read_data()
    if chat_user.get("__version__") != version:
        write_data({
            "__version__": version,
        })
        chat_user = read_data()


@scheduler.scheduled_job("interval", seconds=300)
def save_data():
    write_data(chat_user)


def read_data() -> dict:
    if not store.get_data_file("chatgpt", "data.dat").exists():
        write_data({
            "__version__": version,
        })
    with open(store.get_data_file("chatgpt", "data.dat"), "rb") as file:
        return pickle.load(file)


def write_data(data: dict) -> None:
    with open(store.get_data_file("chatgpt", "data.dat"), "wb") as file:
        pickle.dump(data, file)
