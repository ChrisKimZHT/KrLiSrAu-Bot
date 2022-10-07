from bs4 import BeautifulSoup
from datetime import datetime
import re


async def analy_page(html: str) -> list:
    contest_list = []
    bs = BeautifulSoup(html, "html.parser")
    row_list = bs.find(id="contest-table-upcoming").find("tbody").find_all("tr")
    for row in row_list:
        col_list = row.find_all("td")
        # 日期
        date_utc9 = datetime.strptime(col_list[0].text, "%Y-%m-%d %H:%M:%S%z")
        date_utc8 = date_utc9.astimezone()
        date_str = date_utc8.strftime("%m/%d(%a) %H")
        # 比赛名
        contest_name = col_list[1].a.text
        # 比赛ID
        contest_id = re.findall(r"\d+", contest_name)[-1]
        # 比赛简写
        if re.search(r"Beginner|ABC", contest_name):
            typ = 1
            contest = "ABC" + contest_id
        elif re.search(r"Regular|ARC", contest_name):
            typ = 2
            contest = "ARC" + contest_id
        elif re.search(r"Grand|AGC", contest_name):
            typ = 3
            contest = "AGC" + contest_id
        elif re.search(r"Heuristic|AHC", contest_name):
            typ = 4
            contest = "AHC" + contest_id
        else:
            typ = 0
            contest = "ERROR"
        # 时长
        duration = col_list[2].text
        # 放入列表
        contest_list.append({
            "type": typ,
            "date": date_str,
            "name": contest,
            "dura": duration,
        })
    return contest_list
