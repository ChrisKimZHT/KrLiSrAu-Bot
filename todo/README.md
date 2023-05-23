# todo

管理待办事项

### 功能用法

触发指令：`todo`

```
todo [选项] <内容>
    空 - 显示帮助
    add - 添加待办事项
    list [all] - 显示待办事项
    finish <tid> - 标记待办事项为完成
    del <tid> - 删除待办事项
    clear - 清理所有已完成/过期的待办事项
```

#### 添加待办（交互式）

将会进行交互式新建代办

**示例：**

`todo add`

```
输入事项名称
```

`测试待办 1`

```
输入事项描述
```

`测试描述 1`

```
输入截止时间，格式：YYYY/MM/DD HH:MM
```

`2023/5/2 19:00`

```
添加成功：0
```

#### 添加待办（指令式）

将会进行指令式新建代办

**示例：**`todo create 测试待办1;测试描述1;2023/5/2 19:00`

**结果：**

```
添加成功：0
```

#### 待办列表

将会显示当前待办列表，按时间排序，不包括过期和完成的待办。

若指定 `all` 参数，已过期和已完成的待办也会显示在列表中。

**示例：**`todo list all`

**结果：**

```
用户 15xxxxxx48 的待办事项：
=========================
编号: 0
时间: 2023/05/02 19:00 (0.1 天后)
事项: 测试待办 1
描述: 测试描述 1
=========================
```

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- nonebot_plugin_localstore
- (可选) nonebot_plugin_apscheduler

### 配置项目

| 键名                      | 描述                                                         | 类型      | 默认值 |
| ------------------------- | ------------------------------------------------------------ | --------- | ------ |
| klsa_todo_schedule        | 是否启用定时发送（若启用则必须安装 nonebot_plugin_apscheduler） | bool      | False  |
| klsa_todo_schedule_hour   | 定时小时（crontab 格式）                                     | str       | 9      |
| klsa_todo_schedule_minute | 定时分钟（crontab 格式）                                     | str       | 0      |
| klsa_todo_schedule_group  | 要定时发送的群组号                                           | list[str] | []     |
| klsa_todo_schedule_user   | 要定时发送的私聊 QQ 号                                       | list[str] | []     |