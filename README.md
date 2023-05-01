<div align="center">
  <img src="./banner.png" alt="KrLiSrAu" style="width: 512px" />
</div>

------

基于 [NoneBot2](https://github.com/nonebot/nonebot2) 框架的 QQ 机器人插件，自己写着玩的，实现了一些有趣或实用的功能。各插件互相独立，可自选需要的插件安装。

各插件的具体用法详见插件目录中的 README.md 说明文件。

| 插件名     | 简介                         |
| ---------- | ---------------------------- |
| atcoder    | 查询 AtCoder 比赛信息        |
| bot        | 机器人管理组件               |
| cee        | 查询高考倒计时               |
| cert       | 查询网站 SSL 证书信息        |
| chatgpt    | 基于 OpenAI 接口的聊天机器人 |
| codeforces | 查询 Codeforces 比赛         |
| github     | 查询指定用户 GitHub 贡献图   |
| moyu       | 查询节假日信息               |
| setu       | 基于 Lolicon API 的随机涩图  |

### 安装方式

首先根据 NoneBot2 官方文档创建机器人项目：https://nb2.baka.icu/docs/tutorial/application

注意适配器使用 `nonebot-adapter-onebot-v11`，插件暂无适配其他适配器的计划。

然后将插件放入项目的插件目录，一个文件夹代表一个插件，插件互相独立，可自行选择。

然后查看插件目录下的 README.md 说明文件，使用 pip 安装所需依赖，然后根据说明在配置文件 .env.prod 中填写对应配置项。

最后使用 `nb run` 运行机器人。

