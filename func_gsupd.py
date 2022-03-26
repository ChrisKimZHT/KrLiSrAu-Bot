import datetime

current_version = "2.5"
next_version = "2.6"
current_version_end = "2022-03-30 06:00"
next_version_start = "2022-03-30 11:00"
current_wish_end = "2022-03-29 14:59"
next_wish_start = "2022-03-30 11:00"
current_bp_end = "2022-03-28 04:00"
next_bp_start = "2022-03-30 11:00"
next_sa_start = "2022-04-01 04:00"


def gsupd():
    today = datetime.datetime.now()
    g_end = datetime.datetime.strptime(current_version_end, "%Y-%m-%d %H:%M") - today
    g_start = datetime.datetime.strptime(next_version_start, "%Y-%m-%d %H:%M") - today
    w_end = datetime.datetime.strptime(current_wish_end, "%Y-%m-%d %H:%M") - today
    w_start = datetime.datetime.strptime(next_wish_start, "%Y-%m-%d %H:%M") - today
    bp_end = datetime.datetime.strptime(current_bp_end, "%Y-%m-%d %H:%M") - today
    bp_start = datetime.datetime.strptime(next_bp_start, "%Y-%m-%d %H:%M") - today
    sa_start = datetime.datetime.strptime(next_sa_start, "%Y-%m-%d %H:%M") - today
    result = f"【原神更新】{current_version} -> {next_version}\n"
    result += f"当前版本结束: %02d天 %02d时 %02d分\n" % (g_end.days, g_end.seconds // 3600, g_end.seconds % 3600 // 60)
    result += f"下一版本开始: %02d天 %02d时 %02d分\n" % (g_start.days, g_start.seconds // 3600, g_start.seconds % 3600 // 60)
    result += f"当期祈愿结束: %02d天 %02d时 %02d分\n" % (w_end.days, w_end.seconds // 3600, w_end.seconds % 3600 // 60)
    result += f"下期祈愿开始: %02d天 %02d时 %02d分\n" % (w_start.days, w_start.seconds // 3600, w_start.seconds % 3600 // 60)
    result += f"当期纪行结束: %02d天 %02d时 %02d分\n" % (bp_end.days, bp_end.seconds // 3600, bp_end.seconds % 3600 // 60)
    result += f"下期纪行开始: %02d天 %02d时 %02d分\n" % (bp_start.days, bp_start.seconds // 3600, bp_start.seconds % 3600 // 60)
    result += f"下期深渊开始: %02d天 %02d时 %02d分\n" % (sa_start.days, sa_start.seconds // 3600, sa_start.seconds % 3600 // 60)
    return result
