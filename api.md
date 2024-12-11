请求地址 IP+端口（默认5000）\
例如：0.0.0.0:5000/对应功能的接口地址 \
请在`server.py`找到apikey变量并修改密钥
# 添加配置
地址：`/add/node` \
请求方式 `POST` \
请求类型Headers：`Content-Type:application/json` \
请求Body：
```
port:需要开通的端口号（int）
time：该端口的到期时间（str）
internet：预设流量（int）
apikey：接口密钥（str）

返回 正确200
 "message": "vmess..."
返回 错误200
"message": false
```

# 更新配置信息
地址：`/update/node` \
请求方式 `POST` \
请求类型Headers：`Content-Type:application/json` \
请求Body：
```
port:需要开通的端口号（str）
time：该端口的到期时间 根据类型需要填写（str）
internet：预设流量 根据类型需要填写（int）
type：更新的类型`updatetime`/`updateinternet` 更新时间/更新流量 （str）
apikey：接口密钥（str）

返回 正确200
返回 错误500
```
# 删除配置
地址：`/remove/node` \
请求方式 `POST` \
请求类型Headers：`Content-Type:application/json` \
请求Body：
```
port:需要开通的端口号（int）
apikey：接口密钥（str）

返回 正确200
返回 错误500
```
# 查看配置vmess
地址：`/check/node` \
请求方式 `POST` \
请求类型Headers：`Content-Type:application/json` \
请求Body：

返回 正确200
"message": "vmess..."
返回 错误500
```
port:需要开通的端口号（int）
apikey：接口密钥（str）
```
# 查看配置订阅相关信息
地址：`/check/port` \
请求方式 `POST` \
请求类型Headers：`Content-Type:application/json` \
请求Body：

返回 正确200
"message": "vmess..."
返回 错误500
```
port:需要开通的端口号（int）

返回 正确200
expiration_date 到期时间
flow_information 当前流量消耗信息 packet_count 流量包数目 timestamp 最后更新时间 traffic 流量消耗字节
restrict_traffic 预设流量信息 blocked 是否被阻断（false正常 true被防火墙阻断，一般为超流量或到期）limit 预设流量
返回 错误200、500
```
