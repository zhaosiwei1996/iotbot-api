# iotbot-api

### 宿主机部署:
```
运行环境:Python3.9.6
$ pip install -r requirements.txt
$ python3 iotbot-api.py
```
### 容器部署:
docker-compose.yaml
```
version: '3.3'
services:
  iotbot-data:
    container_name: iotbot-data
    image: iotcore-cn-north-1.jcr.service.jdcloud.com/iotbot/iotbot-api:xx
    environment:
      - DB_NAME=xxxxxx
      - DB_USERNAME=xxxxxx
      - DB_PASSWORD=xxxxxx
      - DB_HOST=mysql-cn-north-1-d47da92a74ee4367.rds.jdcloud.com
      - DB_PORT=3306
      - UVICRON_HOST=0.0.0.0
      - UVICRON_PORT=8000
      - UVICRON_DEBUG=off
      - LOG_LEVEL=info
```
```
$ docker-compose up -d
```

### docker环境变量列表
|名称|说明|参数类型|
|-|-|-|
|DB_NAME |数据库名称 | string |
|DB_PASSWORD |数据库密码 | string |
|DB_HOST |数据库服务器地址 | string |
|DB_PORT |数据库端口 | int |
|UVICRON_HOST |uvicron监听地址 | string |
|UVICRON_DEBUG |uvicron/fastapi debug模式 | string on/off|
|LOG_LEVEL |日志等级 | info/debug/error |

# 接口uri说明
|uri|请求方法|说明|
|-|-|-|
|/api/docs | GET |swagger接口文档 |
|/api/redoc | GET|redoc接口文档 |
|/api| GET |测试接口 |
|/api/user| POST |获取token |
|/api/host/server| GET | 获取服务器数据|
|/api/host/server| PUT | 修改服务器数据|
|/api/host/server/all| GET | 获取服务器所有数据|
|/api/host/proxy/all | GET | 获取服务器所有代理数据|
|/api/host/proxy| GET | 获取服务器代理数据|
|/api/host/proxy| PUT | 修改服务器代理数据|


# 返回状态码说明
|状态码|说明|
|-|-|
|200|ok|
|401|token过期或错误|
|403|密码错误或没有登陆权限|
|404|找不到uri|
|405|请求方法错误|
|422|请求参数错误|
|500|服务器错误|

# 请求示例

### 请求数据接口前,请先登陆获取token(token有效期为1天)

```
curl -XPOST http://localhost/api/user -d {'username':'你的erp账号','password':'你的erp密码加密成md5'}
```
### 返回结果如下:

```
{'rescode': 200, 'msg': '登陆成功', 'timestamp': 1624438985.0702395, 'data': {'username': 'zhaosiwei', 'fullname': '赵
思维', 'token': 'xxxxxxxxxx'}}
```
### 获取其中的token并加上请求头Authorization

### GET方法：
```
curl --header "Authorization:xxxxxx" http://localhost/api/host/server?hostid=&localip=&page=1&size=10 
```
### POST/PUT方法:
```
curl -XPOST/PUT --header "Authorization:xxxxxx" http://localhost/api/host/server -d {
  "hostname": "string",
  "hostid": "string",
  "uniqueid": "string"
}
```


# 返回结果结构示例

### 正常返回
```
{
  "rescode": 200/401/403/500,
  "msg": "xxxxx",
  "timestamp": 1624439106.5643837,
  "data": [根据接口不同返回或为空]
}
```

### 请求参数错误返回
```
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
### 请求方法错误返回
```
{
    "detail": "Method Not Allowed"
}
```
