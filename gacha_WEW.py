from random import randint


# 五星权重函数 W(x) >可修改<
def weight_five(x):
    if x <= 62:
        return 70
    elif 63 <= x <= 73:
        return 70 + 700 * (x - 62)
    elif x >= 74:
        return 7770 + 350 * (x - 73)


# 四星权重函数 W(x) >可修改<
def weight_four(x):
    if x <= 7:
        return 600
    elif x == 8:
        return 6600
    elif x >= 9:
        return 6600 + 3000 * (x - 8)


# 四星平稳机制权重函数 W(x) >可修改<
def weight_stabilizer_four_star(x):
    if x <= 15:
        return 300
    elif x >= 16:
        return 300 + 3000 * (x - 15)


four_star_counter = 1
five_star_counter = 1


# 星级选择器
def star_selector():
    global five_star_counter
    global four_star_counter
    five = weight_five(five_star_counter)
    four = weight_four(four_star_counter)
    three = 9330  # 三星权重 >可修改<
    ceil = 10000  # 权重限制 >可修改<
    wsum = five + four + three  # 权重和
    random_num = randint(1, min(wsum, ceil))  # 随机数生成
    if 1 <= random_num <= five:
        temp = [5, four_star_counter, five_star_counter]
        four_star_counter += 1
        five_star_counter = 1
        return temp
    elif five + 1 <= random_num <= five + four:
        temp = [4, four_star_counter, five_star_counter]
        four_star_counter = 1
        five_star_counter += 1
        return temp
    elif five + four + 1 <= random_num <= five + four + three:
        temp = [3, four_star_counter, five_star_counter]
        four_star_counter += 1
        five_star_counter += 1
        return temp


last_four_up = True
last_five_up = True


# UP选择器
def up_selector(star):
    global last_four_up
    global last_five_up
    if star == 4:
        if last_four_up:
            random_num = randint(1, 100)
            if 1 <= random_num <= 75:  # UP概率 >可修改<
                last_four_up = True
                return True
            else:
                last_four_up = False
                return False
        else:
            last_four_up = True
            return True
    elif star == 5:
        if last_five_up:
            random_num = randint(1, 100)
            if 1 <= random_num <= 75:  # UP概率 >可修改<
                last_five_up = True
                return True
            else:
                last_five_up = False
                return False
        else:
            last_five_up = True
            return True


last_four_star_character = 1
last_four_star_weapon = 1


# 四星类别选择器 True-角色 False-武器
def four_star_type_selector():
    global last_four_star_character
    global last_four_star_weapon
    character = weight_stabilizer_four_star(last_four_star_character)
    weapon = weight_stabilizer_four_star(last_four_star_weapon)
    ceil = 10000  # 权重限制 >可修改<
    wsum = character + weapon  # 权重和
    random_num = randint(1, min(wsum, ceil))  # 随机数生成
    if character == weapon:
        if 1 <= random_num <= character:
            return True
        elif character + 1 <= random_num <= character + weapon:
            return False
    elif character > weapon:
        if 1 <= random_num <= character:
            return True
        elif character + 1 <= random_num <= character + weapon:
            return False
    elif weapon > character:
        if 1 <= random_num <= weapon:
            return False
        elif weapon + 1 <= random_num <= weapon + character:
            return True


# 结果字典
five_star_up = ["雾切之回光", "无工之剑"]
five_star_default = \
    ["阿莫斯之弓", "天空之翼", "四风原典", "天空之卷", "和璞鸢",
     "天空之脊", "狼的末路", "天空之傲", "天空之刃", "风鹰剑"]
four_star_up = ["西风剑", "钟剑", "西风长枪", "西风秘典", "西风猎弓"]
four_star_character = \
    ["云堇", "五郎", "早柚", "托马",
     "烟绯", "罗莎莉亚", "砂糖", "迪奥娜",
     "重云", "诺艾尔", "菲谢尔", "凝光",
     "行秋", "北斗", "香菱", "雷泽",
     "芭芭拉"]
four_star_weapon = \
    ["弓藏", "祭礼弓", "绝弦", "西风猎弓",
     "昭心", "祭礼残章", "流浪乐章", "西风秘典",
     "西风长枪", "匣里灭辰", "雨裁", "祭礼大剑",
     "钟剑", "西风大剑", "匣里龙吟", "祭礼剑",
     "笛剑", "西风剑"]
three_star = \
    ["弹弓", "神射手之誓", "鸦羽弓", "翡玉法球",
     "讨龙英杰谭", "魔导绪论", "黑缨枪", "以理服人",
     "沐浴龙血的剑", "铁影阔剑", "飞天御剑", "黎明神剑",
     "冷刃"]

is_ep = False  # 是否定轨
set_ep = ""  # 当前设置的定规
cnt_ep = -1  # 命定值


# 结果选择器
def result_selector(star, up, typ):
    global is_ep
    global set_ep
    global cnt_ep
    global last_four_star_weapon
    global last_four_star_character
    if star == 3:
        last_four_star_weapon += 1
        last_four_star_character += 1
        return three_star[randint(0, len(three_star) - 1)]
    elif star == 4:
        if up:
            last_four_star_weapon = 1
            last_four_star_character += 1
            return four_star_up[randint(0, len(four_star_up) - 1)]
        else:
            if typ:
                last_four_star_weapon += 1
                last_four_star_character = 1
                return four_star_character[randint(0, len(four_star_character) - 1)]
            else:
                last_four_star_weapon = 1
                last_four_star_character += 1
                return four_star_weapon[randint(0, len(four_star_weapon) - 1)]
    elif star == 5:
        if up:
            res = five_star_up[randint(0, 1)]
            if is_ep:
                if res == set_ep:
                    cnt_ep = 0
                elif cnt_ep == 2:
                    cnt_ep = 0
                    res = set_ep
                else:
                    cnt_ep += 1
            return res
        else:
            res = five_star_default[randint(0, len(five_star_default) - 1)]
            if is_ep:
                if cnt_ep == 2:
                    cnt_ep = 0
                    res = set_ep
                else:
                    cnt_ep += 1
            return res


def wew():
    five_star_list = []  # 五星武器列表
    four_star_character_list = []  # 四型角色列表
    four_star_weapon_list = []  # 四星武器列表
    three_star_list = []  # 三星武器列表
    for i in range(0, 10):
        temp = star_selector()  # 星数选择器返回列表
        star = temp[0]  # 星数
        up = up_selector(star)  # 是否UP
        typ = None
        if star == 4:
            typ = four_star_type_selector()  # 是否为角色
        result = result_selector(star, up, typ)  # 获取具体结果
        # 结果保存
        if star == 3:
            three_star_list.append([result, -1])
        elif star == 4 and typ:
            four_star_character_list.append([result, temp[1]])
        elif star == 4:
            four_star_weapon_list.append([result, temp[1]])
        elif star == 5:
            five_star_list.append([result, temp[2]])
    # 返回结果 高星级角色＞高星级武器＞低星级角色＞低星级武器＞实际抽取顺序
    return five_star_list + four_star_character_list + four_star_weapon_list + three_star_list


def ep(x):
    global is_ep
    global set_ep
    global cnt_ep
    if x == 0:
        is_ep = False
        set_ep = ""
        cnt_ep = -1
        return "【抽卡模拟】定轨：取消"
    elif x == 1:
        is_ep = True
        set_ep = five_star_up[0]
        cnt_ep = 0
        return f"【抽卡模拟】定轨：{set_ep}"
    elif x == 2:
        is_ep = True
        set_ep = five_star_up[1]
        cnt_ep = 0
        return f"【抽卡模拟】定轨：{set_ep}"


def get_epinfo():
    if is_ep:
        return [set_ep, cnt_ep]
    else:
        return ["无", "无"]
