from re import match
from func_moyu import func_moyu
from func_help import func_help
from func_gacha import func_gacha
from func_gsupd import gsupd
from func_cee import cee
from send import send_user, send_group, send_group_at


def keyword_user(message, uid):
    if match(r"^\..*$|^--.*$", message):
        if match(r"^\.help|--help$", message):
            send_user(uid, func_help())
        elif match(r"^\.moyu|--moyu$", message):
            send_user(uid, func_moyu())
        elif match(r"^(\.gacha|--gacha) (?P<type>[0-9]+) (?P<count>[0-9]+)$", message):
            arg = match(r"^(\.gacha|--gacha) (?P<type>[0-9]+) (?P<count>[0-9]+)$", message).groupdict()
            send_user(uid, func_gacha(int(arg["type"]), int(arg["count"])))
        elif match(r"^\.gsupd|--gsupd$", message):
            send_user(uid, gsupd())
        elif match(r"^\.cee|--cee|\.gk|--gk$", message):
            send_user(uid, cee())


def keyword_group(message, uid, gid):
    if match(r"^\..*$|^--.*$", message):
        if match(r"^\.help|--help$", message):
            send_group(gid, func_help())
        elif match(r"^\.moyu|--moyu$", message):
            send_group(gid, func_moyu())
        elif match(r"^(\.gacha|--gacha) (?P<type>[0-9]+) (?P<count>[0-9]+)$", message):
            arg = match(r"^(\.gacha|--gacha) (?P<type>[0-9]+) (?P<count>[0-9]+)$", message).groupdict()
            send_group_at(gid, uid, func_gacha(int(arg["type"]), int(arg["count"])))
        elif match(r"^\.gsupd|--gsupd$", message):
            send_group(gid, gsupd())
        elif match(r"^\.cee|--cee|\.gk|--gk$", message):
            send_group(gid, cee())
