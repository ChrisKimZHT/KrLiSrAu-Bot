import random

with open("./resource/flatterer/flatterer_diary.txt") as file:
    text = file.read().splitlines()
size = len(text)


def flatter():
    global text
    pos = random.randint(0, size - 1)
    return "【舔狗日记】\n" + text[pos]
