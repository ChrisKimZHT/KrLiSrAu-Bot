# bot

机器人管理组件

### 功能用法

触发指令：`bot`

```
bot [选项]
    空 - 显示指令用法
    plugins - 显示所有插件
    help <插件名> - 显示指定插件用法
    exec <语句> - *管理员* 执行shell语句
```

#### 插件列表

将会列出当前机器人已经加载的插件，并分为 ChrisKim 插件（即我开发的插件）与其他插件。

**示例：**`bot plugins`

**结果：**

> 【插件列表】
> \> ChrisKim插件：
> v1.0.0 - bot
> v1.0.3 - moyu
> v1.0.1 - atcoder
> v1.0.2 - github
> v2.0.3 - chatgpt
> v1.0.1 - cert
> v1.0.1 - cee
> v2.0.1 - setu
> v1.0.1 - codeforces
>
> \> 其他插件：
> nonebot_plugin_petpet
> nonebot_plugin_imageutils
> nonebot_plugin_apscheduler
> nonebot_plugin_hikarisearch
> nonebot_plugin_repeater

#### 插件帮助

查询 ChrisKim 插件的使用方式，不支持其他插件。查询时需要使用插件名而不是指令名。

**示例：**`bot help chatgpt`

**结果：**

> 涩图 - 发送随机涩图
> 版本: v2.0.1
> 指令: setu / 涩图
> 用法: setu [标签...] [R18]
>   [标签...] - 指定标签，多个标签用空格分隔
>   [R18] - 指定是否为R18，默认为否

#### [管理员功能] 执行 shell 指令

执行 shell 指令并返回输出。**该功能有安全风险，若要启用，建议使用容器或虚拟机隔离机器人。**

**示例：**`bot exec ls -l`

**结果：**

> 执行结果：
> total 24
> -rw-r--r-- 1 root root 999 Apr  7 17:35 bot.py
> drwxr-xr-x 4 root root   4 Apr  7 17:35 data
> -rw-r--r-- 1 root root 628 Apr  7 17:35 docker-compose.yml
> -rw-r--r-- 1 root root 563 Apr  7 17:36 Dockerfile
> drwxr-xr-x 2 root root   3 Apr  7 17:36 \_\_pycache\_\_
> -rw-r--r-- 1 root root 484 Apr  7 18:18 pyproject.toml
> -rw-r--r-- 1 root root 253 Apr  7 17:36 README.md
> drwxr-xr-x 3 root root   3 Apr  7 18:06 src

### 所需依赖

- nonebot2
- nonebot-adapter-onebot

### 配置项目

| 键名                 | 描述               | 类型 | 默认值 |
| -------------------- | ------------------ | ---- | ------ |
| klsa_bot_exec_enable | 是否启用 exec 功能 | bool | False  |

