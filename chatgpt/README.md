# chatgpt

基于 OpenAI 接口的聊天机器人

### 功能用法

触发指令：`chatgpt` / `chat`

```
chatgpt [选项] <内容>
    <内容> - 进行连续对话
    single <内容> - 进行一次性对话
    setting - 清除对话预设
    setting <内容> - 设置对话预设（会立即初始化）
    len - 查看对话长度（一问一答算一次）
    pop [front/back] - 删除最早/最晚的一次对话
    reset - 重置对话
    bill - 查看额度 
    help - 查看帮助
```

#### 连续对话

与 ChatGPT 进行连续对话，对话实例将会一直保留直到用户手动重置。

由于对话模型具有 token 上限（如 gpt-3.5-turbo 上限 4096 tokens），因此若对话长度超限，返回信息结尾将会提示：[!] 最早的一次对话被删除。

**示例：**`chat 你是谁`

**结果：**

> 请求已发送，等待接口响应...

> 我是一个语言模型AI，由OpenAI创建，可以回答问题、提供建议和聊天等多种功能。
>
> 计算耗时: 22.75 sec
> 单位数量: 45 token(s)
> 消费金额: $0.000090

#### 一次性对话

与 ChatGPT 进行一次性对话，对话完成后，对话实例将会立即删除。

OpenAI 接口将会对历史对话重复计费，因此如果没有连续对话需求，应当使用该功能以节省费用。

**示例：**`chat single 你是谁`

**结果：**

> 请求已发送，等待接口响应...

> 我是一个语言模型AI，由OpenAI创建，可以回答问题、提供建议和聊天等多种功能。
>
> 计算耗时: 22.75 sec
> 单位数量: 45 token(s)
> 消费金额: $0.000090

#### 对话预设

设定一个全局对话预设，对 ChatGPT 风格进行个性化调整（例如调教猫娘）

该全局对话预设将会独立于历史对话列表，不会因对话长度超限而被删除，一定程度上保证 ChatGPT 的风格稳定。

若要清除预设，只需要留空即可。

**示例：**`chat setting [预设内容省略]`

**结果：**

> 请求已发送，等待接口响应...

> [返回内容省略]
>
> 计算耗时: 28.27 sec
> 单位数量: 1260 token(s)
> 消费金额: $0.002520

#### 历史对话控制

若要重置当前对话，使用：`chat reset`

若要查询当前历史对话长度（一问一答算一次），使用：`chat len`

若要删除最早一次对话，使用：`chat pop front`

若要删除最晚一次对话，使用：`chat pop back`

#### 查看额度

查询当前 API Key 的额度信息。该功能需要抓取 OpenAI 账号的 session key（注意不是 secret key），在 https://platform.openai.com/ 登陆后，使用浏览器 F12 工具即可获取。

**示例：**`chat bill`

**结果：**

> 总额度: \$5.00
> 已使用: \$1.12
> 剩余量: \$3.88 (77.6%)

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- aiohttp

### 配置项目

| 键名                  | 描述                | 类型  | 默认值                                                 |
| --------------------- | ------------------- | ----- | ------------------------------------------------------ |
| klsa_chat_api_url     | ChatGPT API 地址    | str   | https://api.openai.com/v1/chat/completions             |
| klsa_chat_api_key     | OpenAI Secret Key   | str   |                                                        |
| klsa_chat_model       | 使用的模型名称      | str   | gpt-3.5-turbo                                          |
| klsa_chat_token_limit | token 限制          | int   | 1024                                                   |
| klsa_chat_kt_cost     | 每 1000 tokens 费用 | float | -1                                                     |
| klsa_bill_api_url     | 查询额度的 API 地址 | str   | https://api.openai.com/dashboard/billing/credit_grants |
| klsa_bill_session     | OpenAI Session Key  | str   |                                                        |