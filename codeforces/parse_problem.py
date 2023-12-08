import aiohttp
from bs4 import BeautifulSoup, NavigableString

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


async def request_html(url: str, lang: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url + f"?locale={lang}", headers=headers) as resp:
            return await resp.text()


def elem_converter(elements: list) -> str:
    result = ""
    for tag in elements:
        if tag.name is None:
            result += tag
        else:
            result += tag.text
    return result


def h_converter(content: list, level: int) -> str:
    prefix = ""
    for i in range(level):
        prefix += "#"
    return f"{prefix} {elem_converter(content)}\n\n"


def p_converter(content: list) -> str:
    return f"{elem_converter(content)}\n\n"


def pre_converter(content: list) -> str:
    return f"```\n{elem_converter(content)}```\n\n"


def blockquote_converter(content: list) -> str:
    result = ""
    for tag in content:
        if tag.name is not None:
            result += f"> {elem_converter(tag.contents)}\n\n"
    return result


def ul_converter(content: list) -> str:
    result = ""
    for tag in content:
        if tag.name == "li":
            result += f"- {elem_converter(tag.contents)}\n"
    return result


def info_converter(content: list) -> str:
    result = ""
    for tag in content:
        if tag.name == "div":
            result += f"{tag.text}: "
        else:
            result += tag
    result += "\n\n"
    return result


def sample_converter(content: list) -> str:
    result = ""
    for tag in content:
        if "input" in (tag.get("class") or []):
            result += "## Input\n\n```\n"
            for ele in tag.pre.contents:
                if ele == "\n":
                    continue
                result += f"{ele.text}\n"
            result += "```\n\n"
        elif "output" in (tag.get("class") or []):
            result += f"## Output\n\n```{tag.pre.text}\n```\n\n"
    return result


def convert(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find(class_="problem-statement")
    result = ""
    for element in sections:
        for tag in element.contents:
            if isinstance(tag, NavigableString):
                result += tag
            elif "title" in (tag.get("class") or []):
                result += h_converter(tag.contents, 1)
            elif "time-limit" in (tag.get("class") or []):
                result += info_converter(tag.contents)
            elif "memory-limit" in (tag.get("class") or []):
                result += info_converter(tag.contents)
            elif "input-file" in (tag.get("class") or []):
                result += info_converter(tag.contents)
            elif "output-file" in (tag.get("class") or []):
                result += info_converter(tag.contents)
            elif "section-title" in (tag.get("class") or []):
                result += h_converter(tag.contents, 1)
            elif "sample-test" in (tag.get("class") or []):
                result += sample_converter(tag.contents)
            elif tag.name == "p":
                result += p_converter(tag.contents)
            elif tag.name == "ul":
                result += ul_converter(tag.contents)

    result = result.replace("$$$", "$")
    return result


async def parse_problem(url: str, lang: str) -> str:
    html = await request_html(url, lang)
    return convert(html)
