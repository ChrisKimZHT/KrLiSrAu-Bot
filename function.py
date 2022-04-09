from re import match
from func_moyu import func_moyu
from func_help import func_help
from func_gacha import func_gacha
from func_ep import func_ep
from func_gsupd import gsupd
from func_cee import cee
from send import send_user, send_group, send_group_at


def keyword_user(message, uid):
    if match(r"^\..*$", message):
        if match(r"^\.help$", message):
            send_user(uid, func_help())
        elif match(r"^\.moyu$", message):
            send_user(uid, func_moyu())
        elif match(r"^\.gacha (?P<type>[1-4]+)$", message):
            arg = match(r"^\.gacha (?P<type>[1-4]+)$", message).groupdict()
            send_user(uid, func_gacha(int(arg["type"])))
        elif match(r"^\.ep (?P<type>[0-2]+)$", message):
            arg = match(r"^\.ep (?P<type>[0-2]+)$", message).groupdict()
            send_user(uid, func_ep(int(arg["type"])))
        elif match(r"^.gsupd$", message):
            send_user(uid, gsupd())
        elif match(r"^\.cee|\.gk$", message):
            send_user(uid, cee())


def keyword_group(message, uid, gid):
    if match(r"^\..*$", message):
        if match(r"^\.help$", message):
            send_group(gid, func_help())
        elif match(r"^\.moyu$", message):
            send_group(gid, func_moyu())
        elif match(r"^\.gacha (?P<type>[1-4]+)$", message):
            arg = match(r"^\.gacha (?P<type>[1-4]+)$", message).groupdict()
            send_group_at(gid, uid, func_gacha(int(arg["type"])))
        elif match(r"^\.ep (?P<type>[0-2]+)$", message):
            arg = match(r"^\.ep (?P<type>[0-2]+)$", message).groupdict()
            send_group(gid, func_ep(int(arg["type"])))
        elif match(r"^.gsupd$", message):
            send_group(gid, gsupd())
        elif match(r"^\.cee|\.gk$", message):
            send_group(gid, cee())
