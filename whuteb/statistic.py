from .storage_manage import read_data, write_data
from .query_data import query_data
import matplotlib.pyplot as plt
import time
from io import BytesIO
from .config import whuteb_config


async def update_statistic():
    data: list = read_data()
    result = await query_data()
    if result["status"]:
        data.append({
            "time": int(time.time()),
            "remain": result["remain"],
            "total": result["total"],
        })
        write_data(data)


def stat_figure() -> BytesIO:
    data_list: list = read_data()[-whuteb_config.klsa_whuteb_history_count:]

    # 从数据列表中获取电费剩余量、当日用电量和对应的日期
    remain = [data["remain"] for data in data_list]
    daily_electricity = [data["total"] - data_list[i - 1]["total"] if i > 0 else 0 for i, data in enumerate(data_list)]
    dates = [time.strftime("%m-%d", time.localtime(data["time"])) for data in data_list]

    # 创建一个包含两个子图的画布
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax2 = ax1.twinx()

    # 绘制电费剩余量的折线图
    ax1.plot(dates, remain, color='orange', label="Remaining Electricity")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Remaining Electricity (kWh)")

    # 绘制当日用电的柱状图
    ax2.bar(dates, daily_electricity, width=0.5, alpha=0.5, label="Daily Electricity Use")
    ax2.set_ylabel("Daily Electricity Use (kWh)")

    # 添加图例
    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax2.legend(lines + bars, labels + bar_labels)

    result = BytesIO()
    fig.savefig(result, format="png")
    return result


def stat_text() -> str:
    result = ""
    data_list: list = read_data()[-whuteb_config.klsa_whuteb_history_count:]
    for data in data_list:
        result += f"{time.strftime('%m-%d', time.localtime(data['time']))} | {data['remain']} kW·h\n"
    return result
