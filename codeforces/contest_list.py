import aiohttp
import time


async def get_list() -> dict:
    api = "https://codeforces.com/api/contest.list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=api) as resp:
            return await resp.json()


async def sort_list(original: dict, count: int) -> list:
    result = []
    for contest in original["result"]:
        if contest["phase"] == "BEFORE":
            result.append(contest)
        else:
            break
    result = sorted(result, key=lambda x: x["startTimeSeconds"])
    while len(result) > count:
        result.pop()
    return result


async def contest_list(res_cnt: int) -> str:
    origin_dict = await get_list()
    sorted_list = await sort_list(origin_dict, res_cnt)
    result = "【Codeforces比赛】\n"
    for contest in sorted_list:
        result += f"{contest['name']}\n" \
                  f"Type: {contest['type']}\n" \
                  f"Duration: {contest['durationSeconds'] // 60} (min)\n" \
                  f"Time: {time.strftime('%Y/%m/%d(%a) %H:%M', time.localtime(contest['startTimeSeconds']))}\n" \
                  f"------------------------------\n"
    return result
