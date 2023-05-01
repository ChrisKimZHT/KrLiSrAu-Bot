# cert

查询网站 SSL 证书信息

### 功能用法

触发指令：`cert` / `ssl` / `证书`

```
cert <域名> - 查询指定域名的证书信息
```

#### 查询 SSL 证书

给出需要查询的域名，通过 curl 查询其证书信息并返回。

**示例：**`cert www.zouht.com`

**结果：**

> 【证书查询】查询成功：
> Server certificate:
> subject: CN=www.zouht.com
> start date: Apr 11 00:00:00 2023 GMT
> expire date: Apr 10 23:59:59 2024 GMT
> subjectAltName: host "www.zouht.com" matched cert's "www.zouht.com"
> issuer: C=US; O=DigiCert Inc; OU=www.digicert.com; CN=Encryption Everywhere DV TLS CA - G1
> SSL certificate verify ok.

### 所需依赖

- nonebot2
- nonebot-adapter-onebot
- (系统环境) curl

### 配置项目

该插件无配置项