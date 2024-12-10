import uuid  # 导入 uuid 模块
import re
import subprocess

# 添加配置
def addV2ray(port):
    # 固定端口号
    port = port

    # 随机生成UUID
    generated_uuid = str(uuid.uuid4())

    # 构建命令
    command = f"v2ray add VMess-TCP {port} {generated_uuid} http"

    # 执行命令并获取输出
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout
        # print("命令执行成功，输出：")
        # print(output)

        # 使用正则表达式提取 vmess:// 后面的 URL
        match = re.search(r'vmess://([A-Za-z0-9+/=]+)', output)
        if match:
            url = match.group(0)  # 获取整个匹配的字符串
            # print("提取到的 URL:", url)
            return url
        else:
            print("未找到 URL")
            return False

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False

# 删除配置
def removev2ray(port):
    # 构建命令
    command = f"v2ray d VMess-TCP-{port}.json"
    try:
        # 执行命令
        subprocess.run(command, shell=True, check=True)
        print(f"删除完毕")
        return True
    except subprocess.CalledProcessError as e:
        print(f"删除完毕")
        return True

# 查看vmess链接
def checkv2ray(port):
    port = port

    command = f"v2ray i VMess-TCP-{port}.json"

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout
        # print("命令执行成功，输出：")
        # print(output)

        # 使用正则表达式提取 vmess:// 后面的 URL
        match = re.search(r'vmess://([A-Za-z0-9+/=]+)', output)
        if match:
            url = match.group(0)  # 获取整个匹配的字符串
            # print("提取到的 URL:", url)
            return url
        else:
            print("未找到 URL")
            return False

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False