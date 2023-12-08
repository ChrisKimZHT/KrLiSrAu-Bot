import aiohttp
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


async def request_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.text()


def var_converter(elements: list) -> str:
    result = ""
    for tag in elements:
        if tag.name is None:
            result += tag
        elif tag.name == "var":
            result += f"${tag.text}$"
        else:
            result += tag.text
    return result


def h3_converter(content: list) -> str:
    return f"### {var_converter(content)}\n\n"


def p_converter(content: list) -> str:
    return f"{var_converter(content)}\n\n"


def pre_converter(content: list) -> str:
    return f"```\n{var_converter(content)}```\n\n"


def blockquote_converter(content: list) -> str:
    result = ""
    for tag in content:
        if tag.name is not None:
            result += f"> {var_converter(tag.contents)}\n\n"
    return result


def ul_converter(content: list) -> str:
    result = ""
    for tag in content:
        if tag.name == "li":
            result += f"- {var_converter(tag.contents)}\n"
    return result


def convert(html: str, lang: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find(id="task-statement").find(class_=f"lang-{lang}").find_all("section")
    result = ""
    for element in sections:
        for tag in element.contents:
            if tag.name == "h3":
                result += h3_converter(tag.contents)
            elif tag.name == "p":
                result += p_converter(tag.contents)
            elif tag.name == "pre":
                result += pre_converter(tag.contents)
            elif tag.name == "blockquote":
                result += blockquote_converter(tag.contents)
            elif tag.name == "ul":
                result += ul_converter(tag.contents)
    return result


async def parse_problem(url: str) -> str:
    html = await request_html(url)
    return convert(html, "en")
