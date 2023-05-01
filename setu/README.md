# setu

发送随机涩图

### 功能用法

触发指令：`setu` / `涩图`

```
setu [标签...] [R18]
    [标签...] - 指定标签，多个标签用空格分隔
    [R18] - 指定是否为R18，默认为否
```

#### 随机涩图

提供 tag，返回随机涩图。返回内容包含作品标题、作者、UID、PID 和图片链接。

**示例：**`setu 迪奥娜`

**结果：**

```
迪奥娜 - 中午茶会
UID: 13693035
PID: 85599270 (p0)
URL: https://i.pximg.net/img-master/img/2020/11/11/11/50/10/85599270_p0_master1200.jpg
```

<img src="https://assets.zouht.com/img/md/KrLiSrAu-Bot-README-02.jpg" style="width: 384px;" />

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- aiohttp
- pillow

### 配置项目

| 键名                        | 描述                                                 | 类型 | 默认值   |
| --------------------------- | ---------------------------------------------------- | ---- | -------- |
| klsa_setu_default_size      | 图片尺寸 (original / regular / small / thumb / mini) | str  | original |
| klsa_setu_proxy_url         | 图片下载时使用的反代地址                             | str  |          |
| klsa_setu_prefix_url        | 发送原图链接时显示的地址                             | str  |          |
| klsa_setu_withdraw_interval | 设置自动撤回，单位秒，若为 0 则不撤回                | int  | 0        |
| klsa_setu_cooldown_time     | 涩图冷却时间，按用户进行计算，单位秒                 | int  | 5        |
| klsa_setu_send_sfw          | 是否发送普通涩图                                     | bool | True     |
| klsa_setu_send_nsfw         | 是否发送 R18 涩图（封号高风险）                      | bool | False    |
| klsa_setu_obfuscate         | 是否开启图片混淆（随机修改图片四角像素，建议开启）   | bool | False    |