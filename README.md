# v2ray-Management
轻量级，管理v2ray服务端流量消耗，一键开通等指令。

# 如何使用
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
