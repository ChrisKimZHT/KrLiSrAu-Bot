# whuteb

武汉理工大学电费监控

### 功能用法

触发指令：`eb`

```
eb [选项]
    空 - 等同于 eb now
    now - 查询当前电费
    stat - 查询电费统计
```

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- nonebot-plugin-localstore
- nonebot-plugin-apscheduler
- matplotlib

### 配置项目

| 键名                               | 描述                         | 类型 | 默认值     |
| ---------------------------------- | ---------------------------- | ---- | ---------- |
| klsa_whuteb_account                | 缴费平台账号                 | str  |            |
| klsa_whuteb_password               | 缴费平台密码                 | str  |            |
| klsa_whuteb_area                   | 校区 (mafangshan / yvjiatou) | str  | mafangshan |
| klsa_whuteb_mafangshan_meterid     | 浏览器调试工具获取 (见下文)  | str  |            |
| klsa_whuteb_mafangshan_factorycode | 浏览器调试工具获取 (见下文)  | str  |            |
| klsa_whuteb_yujiatou_roomno        | 浏览器调试工具获取 (见下文)  | str  |            |
| klsa_whuteb_yujiatou_factorycode   | 浏览器调试工具获取 (见下文)  | str  |            |
| klsa_whuteb_yujiatou_area          | 浏览器调试工具获取 (见下文)  | str  |            |

使用浏览器获取电表号，请参照该仓库文档：https://github.com/ChrisKimZHT/WHUT-EnergyBillMonitor