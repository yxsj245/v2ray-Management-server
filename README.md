# v2ray-Management-server
轻量级，面向销售、开发人员，提供底层管理接口和到期自动暂停等功能

# 特色
通过Linux原生组件实现相关功能，稳定，易上手，搭建简单。
1. 支持通过端口关键参数，一键开通，返回Vmess链接，可搭配前端生成二维码多种形式
2. 支持用户到期自动阻断流量，月底自动彻底删除配置。中途续费仅需使用更新接口即可自动解封。
3. 每月重置流量
4. 可以走按量
6. Qos限速（运行仓库下的sh脚本，或者可以自行编写）

# 如何使用
系统要求：ubuntu centos没测试不保证兼容 \
1. 安装v2ray一键安装脚本[>>点击这里前往](https://github.com/233boy/v2ray)
2. 确保服务器具备python3版本
3. 更新安装需要的pip库
```
pip install --upgrade pip
pip install flask gunicorn
```
3. 确保服务器开启`iptables`防火墙并安装以下组件
```
apt install iptables-persistent
```

# 上传服务器
1. 将本仓库所有源代码以及json文件上传到服务器任意路径
2. 切换到代码所在目录执行
```
python3 订阅管理.py
python3 流量管理.py
gunicorn --reload -w 1 -b 0.0.0.0:5000 server:app
gunicorn --reload -w 1 -b 0.0.0.0:5001 web:app（可选）
```
#### 请注意，上面每个指令对应一个终端服务，请勿全部复制粘贴执行，应当一个个执行并挂入后台
前两条若执行失败，请将`python3`改成`python` \
新手可以搭配MCSManager或其它面板管理各个服务进程

# 文档
[>>API文档](https://github.com/yxsj245/v2ray-Management/blob/server/api.md)
[>>前端项目](https://github.com/yxsj245/v2ray-Management-web)
