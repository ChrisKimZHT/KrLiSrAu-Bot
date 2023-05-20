import aiohttp
from .config import whuteb_config
import json


async def login(session: aiohttp.ClientSession) -> tuple:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "cwsf.whut.edu.cn",
        "Origin": "http://cwsf.whut.edu.cn",
        "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/slogin.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "X-KL-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/userLoginAction!mobileUserLogin.action"
    data = {"nickName": whuteb_config.klsa_whuteb_account, "password": whuteb_config.klsa_whuteb_password}
    async with session.post(url=url, headers=headers, data=data) as response:
        res = json.loads(await response.text())
        if res["returncode"] == "SUCCESS":
            return True, session
        else:
            return False, session


async def mafangshan(session: aiohttp.ClientSession) -> tuple:
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        # "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "JSESSIONID=",
        "Host": "cwsf.whut.edu.cn",
        "Origin": "http://cwsf.whut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/nyyPayElecPages51274E035",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-KL-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/queryReserve"
    data = {"meterId": whuteb_config.klsa_whuteb_mafangshan_meterid,
            "factorycode": whuteb_config.klsa_whuteb_mafangshan_factorycode}
    async with session.post(url=url, headers=headers, data=data) as response:
        respounce = json.loads(await response.text())
        if respounce["returncode"] == "SUCCESS":
            return True, respounce
        else:
            return False, respounce


async def yujiatou(session: aiohttp.ClientSession) -> tuple:
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        # "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "JSESSIONID=",
        "Host": "cwsf.whut.edu.cn",
        "Origin": "http://cwsf.whut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://cwsf.whut.edu.cn/MNetWorkUI/elecdetails51244E023",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-KL-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "http://cwsf.whut.edu.cn/MNetWorkUI/elecManage!querySydl10497"
    data = {"roomno": whuteb_config.klsa_whuteb_yujiatou_roomno,
            "factorycode": whuteb_config.klsa_whuteb_yujiatou_factorycode,
            "area": whuteb_config.klsa_whuteb_yujiatou_area}
    async with session.post(url=url, headers=headers, data=data) as response:
        respounce = json.loads(await response.text())
        if respounce["returncode"] == "SUCCESS":
            return True, respounce
        else:
            return False, respounce


async def query_data() -> dict:
    async with aiohttp.ClientSession() as session:
        status, session = await login(session)
        if status:  # 如果登陆成功
            if whuteb_config.klsa_whuteb_area == "mafangshan":  # 如果是马房山
                status, resp_dict = await mafangshan(session)
                if status:  # 如果请求正常
                    return {
                        "status": True,
                        "remain": float(resp_dict["remainPower"]),
                        "total": float(resp_dict["ZVlaue"]),
                        "time": None,
                    }
            else:  # 如果是余家头
                status, resp_dict = await yujiatou(session)
                if status:  # 如果请求正常
                    return {
                        "status": True,
                        "remain": float(resp_dict["roomlist"]["remainPower"]),
                        "total": float(resp_dict["roomlist"]["ZVlaue"]),
                        "time": resp_dict["roomlist"]["readTime"],
                    }
        return {"status": False}  # 异常情况
