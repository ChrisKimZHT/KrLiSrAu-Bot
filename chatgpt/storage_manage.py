from .chat_class import ChatUser

# 暂时存在内存中，之后再实现持久化
_chat_user = {}


def get_chat_user(user_id: int) -> ChatUser:
    if user_id not in _chat_user:
        _chat_user[user_id] = ChatUser(user_id)
    return _chat_user[user_id]
