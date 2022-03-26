import requests

url = "http://127.0.0.1:5700/send_msg"


def send_user(uid, text):
    data = {
        "user_id": uid,
        "message": text
    }
    requests.get(url, params=data)


def send_group(gid, text):
    data = {
        "group_id": gid,
        "message": text
    }
    requests.get(url, params=data)


def send_group_at(gid, uid, text):
    data = {
        "group_id": gid,
        "message": f"[CQ:at,qq={uid}]" + text
    }
    requests.get(url, params=data)
