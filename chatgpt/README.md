# chatgpt

基于 OpenAI 接口的聊天机器人

### 功能用法

触发指令：`chatgpt` / `chat`

```
chatgpt [选项] <内容>
    <内容> - 进行连续对话
    single <内容> - 进行一次性对话
    reset <预设ID> - 使用预设重置对话
    len - 查看对话长度（一问一答算一次）
    pop [front/back] - 删除最早/最晚的一次对话
    preset - 查看预设列表
    preset add <预设内容> - 添加预设
    preset del <预设ID> - 删除预设
    exec <内容> - 使用ChatGPT调用其他机器人功能
    bill - 查看额度 
    help - 查看帮助
```

#### 连续对话

与 ChatGPT 进行连续对话，对话实例将会一直保留直到用户手动重置。

由于对话模型具有 token 上限（如 gpt-3.5-turbo 上限 4096 tokens），因此若对话长度超限，返回信息结尾将会提示：[!] 最早的一次对话被删除。

可以配置 klsa_chat_timeout 来设置对话实例超时时间，若对话实例超时，会返回 `该对话上次使用时间为2023-05-25 13:07:41，是否重置？(Y/N)` 信息来提示用户。

**示例：**`chat 你是谁`

**结果：**

```
请求已发送，等待接口响应...
```

```
我是一个语言模型AI，由OpenAI创建，可以回答问题、提供建议和聊天等多种功能。

计算耗时: 22.75 sec
单位数量: 45 token(s)
消费金额: $0.000090
```

#### 一次性对话

与 ChatGPT 进行一次性对话，对话完成后，对话实例将会立即删除。

OpenAI 接口将会对历史对话重复计费，因此如果没有连续对话需求，应当使用该功能以节省费用。

**示例：**`chat single 你是谁`

**结果：**

```
请求已发送，等待接口响应...
```

```
我是一个语言模型AI，由OpenAI创建，可以回答问题、提供建议和聊天等多种功能。

计算耗时: 22.75 sec
单位数量: 45 token(s)
消费金额: $0.000090
```

#### 对话预设列表

查看当前已经有的预设列表

**示例：**`chat preset`

**结果：**

```
预设列表：
=========================
0: 我想让你充当 Linux 终端。我将输入...
=========================
1: 我希望你充当 javascript 控制...
=========================
```

#### 添加对话预设

添加新的对话预设

**示例：**`chat preset add 请在之后的回答前加上[test]`

**结果：**

```
添加预设完成
```

#### 删除对话预设

删除指定 ID 的对话预设

**示例：**`chat preset del 2`

**结果：**

```
删除预设完成
```

#### 初始化对话

不附带预设 ID 则不使用预设初始化对话，若附上预设 ID 则使用对应预设初始化对话。预设是独立于消息列表的，永远会固定到消息列表的第一位，并且不会因为 tokens 超限而被删除。

**示例：**`chat reset 1`

**结果：**

```
使用预设 1 重置对话完成：
Hello World
```

#### 历史对话控制

若要查询当前历史对话长度（一问一答算一次），使用：`chat len`

若要删除最早一次对话，使用：`chat pop front`

若要删除最晚一次对话，使用：`chat pop back`

#### 调用其他插件

使用 ChatGPT 来分析对话，生成对应插件的指令从而调用机器人的其他插件。

由于 ChatGPT 很容易不按要求返回导致错误，所以添加 `debug` 参数即可显示 ChatGPT 返回的消息，不添加则不显示。

**示例：**`chat exec 什么时候放假`

**结果：**

```
请求已发送，等待接口响应...
```

```
[debug] ChatGPT返回的信息为：
moyu
```

```
【摸鱼办】23 日晚上好！今天是星期二。
学习再累，一定不要忘记摸鱼哦！累了困了翘水课，上课多去厕所廊道走走，分是老师的，但命是自己的。

☆ 距离周末还有：4 天
☆ 距离端午节还有：30 天
☆ 距离中秋节还有：129 天
☆ 距离国庆节还有：131 天
☆ 距离元旦还有：223 天
☆ 距离春节还有：263 天
☆ 距离清明节还有：318 天
☆ 距离劳动节还有：344 天

学习增加老师负担，摸鱼是给老师减负！最后，祝愿天下所有摸鱼人，都能愉快的度过每一天！
```

#### 查看额度

查询当前 API Key 的额度信息。该功能需要抓取 OpenAI 账号的 session key（注意不是 secret key），在 https://platform.openai.com/ 登陆后，使用浏览器 F12 工具即可获取。

**示例：**`chat bill`

**结果：**

```
总额度: $5.00
已使用: $1.12
剩余量: $3.88 (77.6%)
```

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- aiohttp
- nonebot-plugin-localstore
- nonebot-plugin-apscheduler

### 配置项目

| 键名                            | 描述                           | 类型  | 默认值                                                 |
| ------------------------------- | ------------------------------ | ----- | ------------------------------------------------------ |
| klsa_chat_api_url               | ChatGPT API 地址               | str   | https://api.openai.com/v1/chat/completions             |
| klsa_chat_api_key               | OpenAI Secret Key              | str   |                                                        |
| klsa_chat_model                 | 使用的模型名称                 | str   | gpt-3.5-turbo                                          |
| klsa_chat_token_limit           | token 限制                     | int   | 1024                                                   |
| klsa_chat_timeout               | 对话实例超时限制/秒            | int   | 600                                                    |
| klsa_chat_prompt_token_cost     | 每 1000 prompt tokens 费用     | float | -1                                                     |
| klsa_chat_completion_token_cost | 每 1000 completion tokens 费用 | float | -1                                                     |
| klsa_chat_cooldown              | 冷却时间                       | int   | 0                                                      |
| klsa_chat_bill_api_url          | 查询额度的 API 地址            | str   | https://api.openai.com/dashboard/billing/credit_grants |
| klsa_chat_bill_session          | OpenAI Session Key             | str   |                                                        |
| klsa_chat_exec_prompt           | 调用其他插件的提示词           | str   |                                                        |

注：token 费用请在 https://openai.com/pricing 查询，若不填则不会显示消费金额。

klsa_chat_exec_prompt 的一个示例：

```
你现在是一个机器人助手，你可以通过指令调用别的模块来完成我的请求。你必须严格按照指令格式进行操作，不要附带除了指令之外的任何文字，不要附带任何解释性文本。如果我向你请求的功能不存在，请返回[ERROR](包含中括号)，但不要附上其他任何信息，接下来我会解释功能和指令格式。查询AtCoder算法竞赛的赛程安排，将会返回对应类别比赛的时间等信息: atcoder [选项]，选项留空则为所有比赛，abc为Beginner类别,arc为Regular类别,agc为Grand类别,ahc为Heuristir类别。查询机器人插件列表，将会返回所有插件模块：bot plugins；查询对应年份的高考倒计时：cee <年份>；查询指定网站的SSL证书信息：cert <域名>；查询codeforces算法竞赛的赛程安排，将会返回指定数量的最近比赛，若不指定数量则为默认值：codeforces <数量>；查询指定用户GitHub贡献图：ghc <用户名>；摸鱼办查询节假日信息，将会返回法定节假日的倒计时，如果我问你放假的时间则使用：moyu；查询电费：eb；查询电费统计信息：eb stat；查询待办事项：todo list；添加待办事项：todo create [待办名;备注;YYYY/MM/DD HH:MM](分号隔开，如果没有备注则填无)。下面，我的请求是，注意不要附带除了指令之外的任何文字，不要附带任何解释性文本：
```

