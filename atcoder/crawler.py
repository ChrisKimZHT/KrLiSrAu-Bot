from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re


async def req_page() -> str:
    url = "https://atcoder.jp/contests/"
    headers = {
        "referer": "https://atcoder.jp/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    respounce = requests.get(url, headers=headers).content.decode("UTF-8")
    return respounce


async def get_data(html: str) -> str:
    res = "【Atcoder比赛】\n" \
          "Start Time    | Name   | Dura.\n"
    bs = BeautifulSoup(html, "html.parser")
    table = bs.find(id="contest-table-upcoming").find("tbody").find_all("tr")
    for row in table:
        col_list = row.find_all("td")
        # 日期
        date_9 = datetime.strptime(col_list[0].text, "%Y-%m-%d %H:%M:%S%z")
        date_8 = date_9.astimezone()
        date = date_8.strftime("%m/%d(%a) %H")
        # 比赛名
        contest_name = col_list[1].a.text
        contest_id = re.findall(r"\d+", contest_name)[-1]
        if re.search(r"Beginner|ABC", contest_name):
            contest = "ABC" + contest_id
        elif re.search(r"Regular|ARC", contest_name):
            contest = "ARC" + contest_id
        elif re.search(r"Grand|AGC", contest_name):
            contest = "AGC" + contest_id
        elif re.search(r"Heuristic|AHC", contest_name):
            contest = "AHC" + contest_id
        else:
            contest = "ERROR"
        # 时长
        duration = col_list[2].text
        res += f"{date} | {contest} | {duration}\n"
    return res
