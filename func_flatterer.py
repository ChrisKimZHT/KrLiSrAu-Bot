import random

file = open("./resource/flatterer/flatterer_diary.txt", encoding="UTF-8")
text = file.read().splitlines()
file.close()
size = len(text)


def flatter():
    global text
    pos = random.randint(0, size - 1)
    return "【舔狗日记】\n" + text[pos]
