from re import match
from func_moyu import moyu
from func_help import help
from func_gacha import gacha, ep
from func_gsupd import gsupd
from func_cee import cee
from func_flatterer import flatter
from send import send_user, send_group, send_group_at


def keyword_user(message, uid):
    if match(r"^\..*$", message):
        if match(r"^\.help$", message):
            send_user(uid, help())
        elif match(r"^\.moyu$", message):
            send_user(uid, moyu())
        elif match(r"^\.gacha (?P<type>[1-4]+)$", message):
            arg = match(r"^\.gacha (?P<type>[1-4]+)$", message).groupdict()
            send_user(uid, gacha(int(arg["type"])))
        elif match(r"^\.ep (?P<type>[0-2]+)$", message):
            arg = match(r"^\.ep (?P<type>[0-2]+)$", message).groupdict()
            send_user(uid, ep(int(arg["type"])))
        elif match(r"^.gsupd$", message):
            send_user(uid, gsupd())
        elif match(r"^\.cee|\.gk$", message):
            send_user(uid, cee())
        elif match(r"^\.flatter|\.tg", message):
            send_user(uid, flatter())


def keyword_group(message, uid, gid):
    if match(r"^\..*$", message):
        if match(r"^\.help$", message):
            send_group(gid, help())
        elif match(r"^\.moyu$", message):
            send_group(gid, moyu())
        elif match(r"^\.gacha (?P<type>[1-4]+)$", message):
            arg = match(r"^\.gacha (?P<type>[1-4]+)$", message).groupdict()
            send_group_at(gid, uid, gacha(int(arg["type"])))
        elif match(r"^\.ep (?P<type>[0-2]+)$", message):
            arg = match(r"^\.ep (?P<type>[0-2]+)$", message).groupdict()
            send_group(gid, ep(int(arg["type"])))
        elif match(r"^.gsupd$", message):
            send_group(gid, gsupd())
        elif match(r"^\.cee|\.gk$", message):
            send_group(gid, cee())
        elif match(r"^\.flatter|\.tg", message):
            send_group_at(gid, uid, flatter())
