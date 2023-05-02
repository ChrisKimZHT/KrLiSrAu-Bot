import time


class Todo:
    def __init__(self, name: str, description: str, timestamp: int):
        self.name = name
        self.description = description
        self.timestamp = timestamp

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_timestamp(self) -> int:
        return self.timestamp

    def get_timestr(self) -> str:
        return time.strftime("%Y/%m/%d %H:%M", time.localtime(self.timestamp))

    def is_expired(self) -> bool:
        return self.timestamp < time.time()
